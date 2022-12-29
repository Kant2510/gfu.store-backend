const addProduct = async (req, res, my_database) => {
    const { productId } = req.body

    try {
        my_database.find_push('Carts', { productId: productId }, { userId: req.userId })

        res.json({ success: true, message: 'Add to cart successfully!', productId: productId })
    }
    catch (error) {
        console.log(error)
    }
}

module.exports = addProduct