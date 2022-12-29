
const Login = async (req, res, my_database) => {

    const { username, password } = req.body

    if (!username || !password) {
        return res.json({ success: false, message: 'Missing username or password!', type: 'error' })
    }
    try {
        const hased_password = password + '_hased'

        const matchUser = await my_database.find('Auth', { username })
        const matchPass = await my_database.find('Auth', { password: hased_password })

        if (!matchUser) {
            return res.json({ success: false, message: 'Username is not exist!', type: 'error' })
        }
        if (!matchPass) {
            return res.json({ success: false, message: 'Wrong password!', type: 'error' })
        }

        res.json({ success: true, message: 'Login successfully!', type: 'success' })
    }
    catch (error) {
        return res.json({ success: false, message: error, type: 'error' })
    }
}

module.exports = Login