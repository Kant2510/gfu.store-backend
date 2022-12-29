const express = require('express')
const router = express.Router()
const Register = require('../Controllers/register')

const authRegister = my_database => {

    router.post('/', (req, res) => Register(req, res, my_database))

    return router
}

module.exports = authRegister