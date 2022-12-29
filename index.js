const Database = require('./Models/Database/index.js')
const express = require('express')
const cors = require('cors')
const authRegister = require('./Routes/register')
const authLogin = require('./Routes/login.js')
const addProductToCart = require('./Routes/addProduct.js')

const url = process.env.dbUrl
const dbName = 'GFU-STORE'
const my_database = new Database(url, dbName)

my_database.connect()

const app = express()

app.use(express.static('public'))
app.use(cors())
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

app.get('/', (req, res) => {
    res.send('haha')
})

app.use('/auth/register', authRegister(my_database))

app.use('/auth/login', authLogin(my_database))

app.use('/auth/add', addProductToCart(my_database))

const PORT = 5000

app.listen(PORT, () => console.log(`Server started on port ${PORT}`))

