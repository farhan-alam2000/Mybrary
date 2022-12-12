// const authApp = require("../server")
const router = require("express").Router();
const User = require("../models/user");
const Author = require("../models/author");
// const bcrypt = require('bcrypt');
const bcrypt = require('bcryptjs');
const passport = require('passport');
const { forwardAuthenticated } = require('../config/auth');

//view registration page
router.get("/register", forwardAuthenticated, async (req, res) => {
    res.render('auth/register', {layout: "layouts/layout2"})
})

// REGISTER a new user
router.post("/register", async (req, res) => {
    try {
        // console.log(req.body)
        const pass = req.body.password;
        const username = req.body.username;
        const email = req.body.email;
        console.log(email);
        if(pass.length < 4)
            res.status(400).json("Password must be atleast 4 characters long");

        if(username.length == 0)
            res.status(400).json("Enter username");
        
        if(email.length == 0)
            res.status(400).json("Enter email");
        
        console.log(1);
        const salt = await bcrypt.genSalt(10);
        const hashedPass = await bcrypt.hash(req.body.password, salt);

        console.log(2);
        const user = await User.findOne({username: req.body.username});
        if(user) {
            res.redirect('/auth/register')
        }

        const user2 = await User.findOne({email: req.body.email});
        if(user2) {
            res.redirect('/auth/register')
        }

        console.log(3);
        const newUser = new User({
            username: req.body.username,
            email: req.body.email,
            password : hashedPass
        });
        const newAuthor = new Author({
            name: req.body.username
        })

        userPut = await newUser.save();  // users will be the collection
        await newAuthor.save(); //user is also an author
        
        // in which this user will get added (MongoDB plural thingy)
        // console.log(userPut);
        // res.status(200).json(userPut);
        res.redirect('/auth/login')
    } catch (err) {
        console.log("NOOOOOO");
        // res.status(500).json(err);
        res.redirect('/auth/register');
    }
});

// view login page
router.get("/login", forwardAuthenticated, async (req, res) => {
    res.render('auth/login', {layout: "layouts/layout2"})
})

// LOGIN
router.post('/login',passport.authenticate('local', { failureRedirect: '/auth/login', failureFlash: true }), (req, res, next) => {
    // console.log(global.email)
    global.email = req.body.email
    res.redirect('/')
    // res.redirect('/index/' + req.body.email)
    // passport.authenticate('local', {
    //   successRedirect: '/',
    //   failureRedirect: '/auth/login',
    //   failureFlash: true
    // })(req, res, next);
});

// router.post('/login',passport.authenticate('local', { failureRedirect: '/auth/login', failureFlash: true }), async (req, res, next) => {
//     const email = req.body.email
//   // console.log(query.Email)
// //   console.log(req.params.id)
//   let books
//   try {
//     books = await Book.find({email}).sort({ createdAt: 'desc' }).limit(10).exec()
//   } catch {
//     books = []
//   }
//   res.render('index', { books: books, email: email })
// });



//logout
router.get('/logout', (req, res) => {
    // req.logout();
    // req.flash('success_msg', 'You are logged out');
    // res.redirect('/auth/login');
    req.logOut((err)=>{
    if(err){
      return next(err)
    }
    req.flash('success_msg', 'You are logged out');
    res.redirect('/auth/login')
  })
});

// app.delete('/logout', (req, res) => {
//   req.logOut((err)=>{
//     if(err){
//       return next(err)
//     }
//     res.redirect('/login')
//   })
// })

module.exports = router






