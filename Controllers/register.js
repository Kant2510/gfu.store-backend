require('dotenv').config()
const jwt = require('jsonwebtoken')

const Register = async (req, res, my_database) => {

    const { fullname, username, password, repeat, email, phone } = req.body

    if (!fullname || !username || !password || !repeat || !email || !phone) {
        return res.json({ success: false, message: 'Missing requested information!', type: 'error' })
    }
    if (password !== repeat) {
        return res.json({ success: false, message: 'Password does not match!', type: 'error' })
    }
    try {

        const matchUser = await my_database.find('Auth', { username })

        if (matchUser) {
            return res.json({ success: false, message: 'Username already taken!', type: 'error' })
        }

        const hased_password = password + '_hased'

        const userInfo = await my_database.add('Auth', { fullname, username, password: hased_password, email, phone, date: new Date })

        const accessToken = jwt.sign({ userId: userInfo.insertedId.toString() }, process.env.secret)
        console.log(accessToken)
        res.json({ success: true, message: 'Register successfully!', type: 'success', accessToken })
    }
    catch (error) {
        console.log(error)
        return res.json({ success: false, message: error, type: 'error' })
    }
}

module.exports = Register