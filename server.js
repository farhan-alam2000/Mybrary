if (process.env.NODE_ENV !== 'production') {
  require('dotenv').load()
}

const express = require('express')
const app = express()
const expressLayouts = require('express-ejs-layouts')
const bodyParser = require('body-parser')
const methodOverride = require('method-override')

const mongoose = require('mongoose')
mongoose.connect(process.env.DATABASE_URL, { useNewUrlParser: true })
const db = mongoose.connection
db.on('error', error => console.error(error))
db.once('open', () => console.log('Connected to Mongoose'))


const indexRouter = require('./routes/index')
const authorRouter = require('./routes/authors')
const bookRouter = require('./routes/books')
const authRouter = require('./routes/auth')

app.set('view engine', 'ejs')
app.set('views', __dirname + '/views')
app.set('layout', 'layouts/layout', 'layouts/layout2')
app.use(expressLayouts)
app.use(methodOverride('_method'))
app.use(express.static('public'))
app.use(bodyParser.urlencoded({ limit: '10mb', extended: false }))
app.use(express.urlencoded( {extended: false} ))

app.use('/', indexRouter)
app.use('/authors', authorRouter)
app.use('/books', bookRouter)
app.use('/auth', authRouter)

// app.delete('/logout', (req, res) => {
//   req.logOut((err)=>{
//     if(err){
//       return next(err)
//     }
//     res.redirect('/login')
//   })
// })

app.listen(process.env.PORT || 3000)