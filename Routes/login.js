const express = require('express')
const router = express.Router()
const Login = require('../Controllers/login')

const authLogin = my_database => {

    router.post('/', async (req, res) => { Login(req, res, my_database) })
    return router
}

module.exports = authLogin