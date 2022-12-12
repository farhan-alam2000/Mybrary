const mongoose = require("mongoose")

const userSchema = new mongoose.Schema({
    username:{
        type: String,
        required: true,
        unique: true
    },email: {
        type: String,
        required: true,
        unique: true
    },
    password: {
        type: String,
        required: true
    },
    index: {
        type: String,
        required: false
    },
    date: {
        type: Date,
        default: Date.now
    },
    doc_no: {
        type: Number,
        default: 0
    }
})

module.exports = mongoose.model('User', userSchema);