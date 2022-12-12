const express = require("express");
const router = express.Router();
const Book = require("../models/book");
const Author = require("../models/author");
// const { ensureAuthenticated, forwardAuthenticated } = require('../config/auth');
const imageMimeTypes = ["image/jpeg", "image/png", "images/gif"];
const { spawn, spawnSync } = require("child_process");
const User = require("../models/user")

// All Books Route and Search Route
router.get("/", async (req, res) => {
  const email = global.email
  
  let query = Book.find({email});
  // console.log(query)
  // console.log(query.schema.obj.email)
  if (req.query.title != null && req.query.title != "") {
    query = query.regex("title", new RegExp(req.query.title, "i"));
  }
  if (req.query.publishedBefore != null && req.query.publishedBefore != "") {
    query = query.lte("publishDate", req.query.publishedBefore);
  }
  if (req.query.publishedAfter != null && req.query.publishedAfter != "") {
    query = query.gte("publishDate", req.query.publishedAfter);
  }

  try {
    // console.log(email)
    const books = await query.exec();
    // console.log(books)
    res.render("books/index", {
      books: books,
      searchOptions: req.query,
    });
    
    if (req.query.title != null && req.query.title != "") {
      // const keyword = req.query.title; //case sensitive?
      const keyword = "India"; //case sensitive?
      const trapdoor = spawnSync("python", [
        "C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/trapdoor.py",
        keyword,
      ]);
      console.log("Trapdoor executed")
      console.log(trapdoor.output.toString('utf-8'));

      const search = spawnSync("python", [
        "C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/search.py",
        keyword,
      ]);
      // dataToSend = search.output.toString('utf-8')
      console.log(search.output.toString('utf-8'));
    }

  } catch {
    res.redirect("/");
  }
});

// New Book Route
router.get("/new", async (req, res) => {
  renderNewPage(res, new Book());
});

// Create Book Route
router.post("/", async (req, res) => {
  try {
    // const newBook = await book.save();
    // res.redirect(`books/${newBook.id}`);
    const data = req.body.description; //we can send title also to script
    // do this update route 
    // const data = "America, officially the Republic of India, is a country in South Asia." 
    // const email = global.email
    const email = "farhan@gmail.com"
    const user = await User.find({email})
    // console.log(user[0].password)
    const password = user[0].password.slice(0,16)
  
  //CLEAN THE TEXT
  const preprocess = spawnSync("python", ["C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/preprocess.py", data]);
  const cleaned_doc = preprocess.output.toString('utf8');
    console.log(cleaned_doc)
  //Encrypt the Text
  const encryptingDoc = spawnSync("python", ["C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/encrypt_text.py", cleaned_doc, password]);
  const encr_text = encryptingDoc.output.toString('utf8');
  console.log(encr_text)
  
  const newBook = new Book({
    email: email,
    title: req.body.title,
    description: encr_text,
  });
  saveCover(newBook, req.body.cover);
  //Saving the Encrypted Text
  newBook
    .save()
    .then((savedText) => {
      const id = savedText._id.toString(); 
      console.log("encrypted text is saved!", "id is ", id)

      //Creating the Index Table
      const indexing = spawnSync("python", [
        "C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/indexing.py",
        cleaned_doc, id
      ]);
      const idx_table = indexing.output.toString('utf8');
      // console.log(idx_table)
      //Encrypting the Index Table
      const encrypt = spawnSync("python", [
        "C:/Users/alaam/OneDrive/Desktop/mybrary/Mybrary/public/pythonScripts/encrypt_index.py", idx_table, password
      ]);
      const encr_idx = encrypt.output.toString('utf8')
      console.log(encr_idx)
      //Saving the Encrypted Table
      User.findOneAndUpdate({email: email}, {index:encr_idx}, {new:true})
      .catch(err => console.log(err))

      res.redirect(`books/${id}`);
    })
    .catch((err) => console.log(err));
    
  } catch(err) {
    console.log(err)
    renderNewPage(res, newBook, true);
  }
});

// Show Book Route
router.get("/:id", async (req, res) => {
  try {
    const book = await Book.findById(req.params.id).populate("author").exec();
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
