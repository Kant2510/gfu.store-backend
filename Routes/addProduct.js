const express = require('express')
const router = express.Router()
const verifyToken = require('../Middleware/auth')
const addProduct = require('../Controllers/addProduct')

const addProductToCart = my_database => {

    router.post('/', verifyToken, async (req, res) => { addProduct(req, res, my_database) })
    return router
}

module.exports = addProductToCart