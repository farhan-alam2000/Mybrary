const express = require('express')
const app = express()
const router = express.Router()
const Book = require('../models/book')
const { ensureAuthenticated, forwardAuthenticated } = require('../config/auth');

router.get('/', ensureAuthenticated, async (req, res) => {
  const email = global.email
  let books
  try {
    books = await Book.find({email}).sort({ createdAt: 'desc' }).limit(10).exec()
  } catch {
    books = []
  }
  res.render('index', { books: books })
})

module.exports = router