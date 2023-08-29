def responeForm(
    success,
    message,
    type,
    token=None,
    user=None,
    cart=None,
    products=None,
    discounts=None,
):
    response = {"success": success, "message": message, "type": type}
    if token is not None:
        response["token"] = token
    if user is not None:
        response["user"] = user
    if cart is not None:
        response["cart"] = cart
    if products is not None:
        response["products"] = products
    if discounts is not None:
        response["discounts"] = discounts
    return response
