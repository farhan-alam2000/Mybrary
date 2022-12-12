// const express = require("express");
// const app = express();
// const session = require("express-session");
// app.use(
//   session({
//     secret: "keyboard cat",
//     resave: false,
//     saveUninitialized: true,
//     cookie: { secure: true },
//   })
// );
// app.use(express.static("public"));

// app.get("/show/:id", (request, response, next) => {
// //   request.session.id = request.params.id;
//   response.send("ID stored")
// });

// //Retrieve the id from the session object.
// app.get("/showMyId", (request, response, next) => {
//     // console.log(request.session.id)
//   response.send(request.session.id);
// });

// const PORT = 3000

// app.listen(PORT, console.log(`Server running on  ${PORT}`));

