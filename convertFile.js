if (process.env.NODE_ENV !== "production") {
    require("dotenv").load();
}
const fs = require('fs')
const CSVtoJSON = require('csvtojson');
const { mongo } = require('mongoose');
const JSONtoCSV = require('json2csv').parse

const mongoose = require("mongoose");

mongoose.connect(process.env.DATABASE_URL, { useNewUrlParser: true });
const db = mongoose.connection;
db.on("error", (error) => console.error(error));
db.once("open", () => console.log("Connected to Mongoose"));

const csvSchema = new mongoose.Schema({
    email: {
        type: String,
        required: true
    },
    indexTable: [
        {
            type: Object
        }
    ] 
})


const CSV = mongoose.model('CSV', csvSchema);
/*
CSVtoJSON().fromFile("./yes_index.csv").then(source => {
    // console.log(source)
    // console.log(source[0])
    // console.log(Object.keys(source[0])) //getting all keys
    // source.push(
    //   {
    //     field1: '51',
    //     keyword: `b'_K\\xf1\\x86\\xefI"W\\x90\\x95\\xed\\xa3g\\xc4\\xdf\\xe3'`,
    //     doc_1: "b'T\\xbb\\xd1q\\x8b\\x98/\\xed\\x90\\x04\\x8dR\\x1c\\xb3N\\xc5'",
    //     doc_2: "b'B#l\\x9bJc3\\x85\\xdb,\\xf3ri\\xd2i!'",
    //     doc_3: "b'T\\xbb\\xd1q\\x8b\\x98/\\xed\\x90\\x04\\x8dR\\x1c\\xb3N\\xc5'",
    //     doc_4: "b'T\\xbb\\xd1q\\x8b\\x98/\\xed\\x90\\x04\\x8dR\\x1c\\xb3N\\xc5'"
    //   }
    // )
    const email = "farhan@gmail.com"
    const newCSV = new CSV({
        email: email,
        indexTable: source
    })
    newCSV.save().then(
        console.log("csv saved to DB")
    )
    // const csv = JSONtoCSV(source, { feilds: Object.keys(source[0]) })
    // fs.writeFileSync("./dest.csv", csv)
    //in our system delete file after converting to json
});
*/
async function saveCSVtoDB(){
    const source = await CSVtoJSON().fromFile("./yes_index.csv");
    // console.log(source)
    // console.log(source[0])
    // console.log(Object.keys(source[0])) //getting all keys
    const email = "farhan@gmail.com"
    const newCSV = new CSV({
        email: email,
        indexTable: source
    })

    await newCSV.save()
    console.log("csv saved to DB");
}

async function getCSVfromDB(){
    const email = "farhan@gmail.com"
    const csvObj = await CSV.findOne({email})
    // console.log(csvObj)
    // console.log(csvObj.indexTable)
    const source = csvObj.indexTable
    const csv = JSONtoCSV(source, { feilds: Object.keys(source[0]) })
    fs.writeFileSync("./dest" + csvObj._id + ".csv", csv)
    const fileName = "./dest" + csvObj._id;
    return fileName; //pass it to python script
}

// saveCSVtoDB()
getCSVfromDB()