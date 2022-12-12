const express = require('express')
const app = express()
const router = express.Router()
const Book = require('../models/book')
const { ensureAuthenticated, forwardAuthenticated } = require('../config/auth');



router.get('/', ensureAuthenticated, async (req, res) => {
  const email = global.email
  // console.log(query.Email)
  // console.log(req.params.id)
  let books
  try {
    books = await Book.find({email}).sort({ createdAt: 'desc' }).limit(10).exec()
    for(let i = 0; i < books.length; i++)
    {
      books[0].title = books[0].title.slice(26)
    }
  } catch {
    books = []
  }
  res.render('index', { books: books, email: email })
})
// router.get('/index/:id', ensureAuthenticated, async (req, res) => {
//   const email = req.params.id
//   global.email = email
//   // console.log(query.Email)
//   console.log(req.params.id)
//   let books
//   try {
//     books = await Book.find({email}).sort({ createdAt: 'desc' }).limit(10).exec()
//   } catch {
//     books = []
//   }
//   res.render('index', { books: books, email: email })
// })

module.exports = router