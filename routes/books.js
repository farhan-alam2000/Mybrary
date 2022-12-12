const express = require("express");
const router = express.Router();
const fs = require("fs");
const CSVtoJSON = require("csvtojson");
const JSONtoCSV = require("json2csv").parse;
//Checking the crypto module
const crypto = require('crypto');
const algorithm = 'aes-256-cbc'; //Using AES encryption
const key = crypto.randomBytes(32);
const iv = crypto.randomBytes(16);
// const key = <Buffer ce 1a b0 d2 78 f3 80 45 aa 53 1a e9 b8 ce 41 70 ea 12 34 a6 f3 25 25 70 46 6f d4 ca 26 c9 0e 59>;
// const iv = crypto.randomBytes(16);

const Book = require("../models/book");
const Author = require("../models/author");
// const { ensureAuthenticated, forwardAuthenticated } = require('../config/auth');
const imageMimeTypes = ["image/jpeg", "image/png", "images/gif"];
const { spawn, spawnSync } = require("child_process");
const User = require("../models/user");

// All Books Route and Search Route
router.get("/", async (req, res) => {
  const email = global.email;
  // console.log(req.body.email + "from book route")
  // let query = Book.find({email});
  // // console.log(query)
  // // console.log(query.schema.obj.email)
  // if (req.query.title != null && req.query.title != "") {
  //   query = query.regex("title", new RegExp(req.query.title, "i"));
  // }
  // if (req.query.publishedBefore != null && req.query.publishedBefore != "") {
  //   query = query.lte("publishDate", req.query.publishedBefore);
  // }
  // if (req.query.publishedAfter != null && req.query.publishedAfter != "") {
  //   query = query.gte("publishDate", req.query.publishedAfter);
  // }

  try {
    if (req.query.title == null || req.query.title == "") {
      const books = []
      res.render("books/index", {
        books: books,
        searchOptions: req.query,
      });
    }
    
    if (req.query.title != null && req.query.title != "") {
      let keyword = req.query.title; 
      keyword = keyword.toLowerCase()
      const user = await User.find({ email });
      // console.log(user[0].password)
      const password = user[0].password.slice(0, 16);

      //CLEAN THE KEYWORDS
      // const preprocess = spawnSync("python", ["D:/work/BTP/CODE/Main/preprocess.py", keyword]);
      // const cleaned_keyword = preprocess.output.toString('utf8');
      // console.log(cleaned_keyword)


      const trapdoor = spawnSync("python", [
        "C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/trapdoor.py",
        keyword,
        password,
      ]); //trapdoors.csv
      const trapdoor_set = trapdoor.output.toString("utf-8");
      console.log("trapdoor.py says : " + trapdoor_set);

      User.find({ email: email })
        .then((user) => {
          const ind_table = user[0].index;
          const search = spawnSync("python", [
            "C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/search.py",
            trapdoor_set,
            ind_table,
          ]); //returns index number
          const search_res = search.output.toString("utf-8");
          console.log("search.py says : " + search_res);
          // console.log("\n" + search_res + "\n");
          // res.send(search_res)
          if (search_res == ",-1") console.log("Do nothing");

          const userID = user[0]._id;
          const fetchArray = spawnSync("python", [
            "C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/findnsort.py",
            search_res,
            // userID,
          ]); //return results.csv
          const documents = fetchArray.output.toString("utf-8");
          console.log("findnsort.py says : " + documents);

          // const fileName = "results" + userID + ".csv";
          const fileName = "results.csv";
          CSVtoJSON()
            .fromFile(fileName)
            .then( async (resultJson) => {
              console.log(resultJson);
              const bookIDs = []

              for(let i = 0; i < resultJson.length; i++){
                const bookID = resultJson[i].Heading;
                if(bookID.length > 0){
                  bookIDs.push(bookID)
                }
              }
              console.log(bookIDs)
              // let books = []
              // Book.collection.find( { _id : { $in : bookIDs } } ).then( books => {
              //     console.log(books)
              //     res.render("books/index", {
              //       books: books,
              //       searchOptions: req.query,
              //     });
              // })
              let books = []
              // let titles = []
              for(let i = 0; i < bookIDs.length; i++)
              {
                let book = await Book.find({ _id : bookIDs[i] })
                // titles.push(book.title.slice(20)) //decryption
                book[0].title = book[0].title.slice(26)
                // console.log(sliced)
                // book.title = book.title.slice(20)
                books.push(book[0])
              }
              console.log(books)
              res.render("books/index", {
                books: books,
                searchOptions: req.query,
              });
              // Book.find({ _id : bookIDs[0] }).then( books => {
              //     console.log(books)
              //     res.render("books/index", {
              //       books: books,
              //       searchOptions: req.query,
              //     });
              // })
            })
              // res.send("Hey")
        });

          // res.send(documents)
          // res.redirect('/books/index')
          // res.render('books/index', {
          //   books: book,
          //   searchOptions: req.query
          // })
          // res.render("books/index", {
          //   books: books,
          //   searchOptions: req.query,
          // });
        // })
        // .catch((err) => console.log(err));
    // }
    } 
  } catch {
    res.redirect("/");
  }
});

// New Book Route
router.get("/new", async (req, res) => {
  renderNewPage(res, new Book());
});

//Encrypting text
function encrypt(text) {
  let cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key), iv);
  let encrypted = cipher.update(text);
  encrypted = Buffer.concat([encrypted, cipher.final()]);
  return { iv: iv.toString('hex'), encryptedData: encrypted.toString('hex') };
}

// Create Book Route
router.post("/", async (req, res) => {
  try {
    // const newBook = await book.save();
    // res.redirect(`books/${newBook.id}`);

    const data = req.body.title; //we can send title also to script
    // do this update route
    // const data = "America, officially the Republic of India, is a country in South Asia."
    const email = global.email;
    // const email = "farhan@gmail.com"
    const user = await User.find({ email });
    // console.log(user[0].password)
    const password = user[0].password.slice(0, 16);
    const docNo = user[0].doc_no;

    //CLEAN THE TEXT
    const preprocess = spawnSync("python", [
      "C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/preprocess.py",
      data,
    ]);
    const cleaned_doc = preprocess.output.toString("utf8");
    console.log(cleaned_doc);
    //Encrypt the Text
    /*
    const encryptingDoc = spawnSync("python", [
      "C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/encrypt_text.py",
      data,
      password,
    ]);
    let encr_text = encryptingDoc.output.toString("utf8");
    encr_text = encr_text.slice(1)
    console.log("from encr text : ", encr_text);
    // encr_text = encr_text.hex()
    //convert index.csv to json and store in DB
    */
    // const encr_text = encrypt(data)
    let str = ""
    if(data.length >= 3){
      for(let i = 0; i <= 2; i++)
      {
        str += data[i] + '26'
      }
    }
    const encr_text = str + '7QCKUGhvdG9za7bhd' + data; //20 + data
    console.log(encr_text)
    
    const newBook = new Book({
      email: email,
      title: encr_text,
      description: req.body.description,
    });
    saveCover(newBook, req.body.cover);
    //Saving the Encrypted Text
    
    console.log("THE DOCUMENT NUMBER I GIVE IS ", docNo)

    newBook
      .save()
      .then((savedText) => {
        const id = savedText._id.toString();
        console.log("encrypted text is saved!", "id is ", id);
        //Creating the Index Table
        const indexing = spawnSync("python", [
          "C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/indexing.py",
          cleaned_doc,
          id,
          docNo
        ]);
        const idx_table = indexing.output.toString("utf8");
        console.log("table  is ",idx_table)
        //Encrypting the Index Table
        const encrypt = spawnSync("python", [
          "C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/encrypt_index.py",
          idx_table,
          password,
        ]);
        const encr_idx = encrypt.output.toString("utf8");
        // console.log(encr_idx);
        //Saving the Encrypted Table
        
        User.findOneAndUpdate(
          { email: email },
          {index:encr_idx, doc_no: docNo+1},
          { new: true },
        ).catch((err) => console.log(err));

        res.redirect(`books/${id}`);
      })
      .catch((err) => console.log(err));
  } catch (err) {
    console.log(err);
    renderNewPage(res, newBook, true);
  }
});

// Show Book Route
router.get("/:id", async (req, res) => {
  try {
    const book = await Book.findById(req.params.id).populate("author").exec();
    book.title = book.title.slice(26)
    /*
    const data = book.title;
    console.log("show book data : " + data)
    const user = await User.find({ email });
    // console.log(user[0].password)
    const password = user[0].password.slice(0, 16);
    
    const decryptingDoc = spawnSync("python", [
      "C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/decrypt_text.py",
      data,
      password,
    ]);
    const decr_text = decryptingDoc.output.toString("utf8");
    console.log("show book decrpted text : " + decr_text);
    */
    res.render("books/show", { book: book });
  } catch {
    res.redirect("/");
  }
});

// Edit Book Route
router.get("/:id/edit", async (req, res) => {
  try {
    const book = await Book.findById(req.params.id);
    renderEditPage(res, book);
  } catch {
    res.redirect("/");
  }
});

// Update Book Route
router.put("/:id", async (req, res) => {
  let book;

  try {
    book = await Book.findById(req.params.id);
    book.title = req.body.title;
    // book.author = req.body.author;
    // book.publishDate = new Date(req.body.publishDate);
    // book.pageCount = req.body.pageCount;
    book.description = req.body.description;
    if (req.body.cover != null && req.body.cover !== "") {
      saveCover(book, req.body.cover);
    }
    await book.save();
    res.redirect(`/books/${book.id}`);
  } catch {
    if (book != null) {
      renderEditPage(res, book, true);
    } else {
      redirect("/");
    }
  }
});

// Delete Book Page
router.delete("/:id", async (req, res) => {
  let book;
  try {
    book = await Book.findById(req.params.id);
    await book.remove();
    res.redirect("/books");
  } catch {
    if (book != null) {
      res.render("books/show", {
        book: book,
        errorMessage: "Could not remove book",
      });
    } else {
      res.redirect("/");
    }
  }
});

async function renderNewPage(res, book, hasError = false) {
  renderFormPage(res, book, "new", hasError);
}

async function renderEditPage(res, book, hasError = false) {
  renderFormPage(res, book, "edit", hasError);
}

async function renderFormPage(res, book, form, hasError = false) {
  try {
    const authors = await Author.find({});
    const params = {
      authors: authors,
      book: book,
    };
    if (hasError) {
      if (form === "edit") {
        params.errorMessage = "Error Updating Book";
      } else {
        params.errorMessage = "Error Creating Book";
      }
    }
    res.render(`books/${form}`, params);
  } catch {
    res.redirect("/books");
  }
}

function saveCover(book, coverEncoded) {
  if (coverEncoded == null) return;
  const cover = JSON.parse(coverEncoded);
  if (cover != null && imageMimeTypes.includes(cover.type)) {
    book.coverImage = new Buffer.from(cover.data, "base64");
    book.coverImageType = cover.type;
  }
}

module.exports = router;
