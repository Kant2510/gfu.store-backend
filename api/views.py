from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Product, Account, Cart, DiscountCode
from .serializers import (
    AccountSerializer,
    ProductSerializer,
    RegisterSerializer,
    LoginSerializer,
    CartSerializer,
    DiscountCodeSerializer,
)
from rest_framework.authtoken.models import Token
from .respone import responeForm

# Create your views here.


@api_view(["GET"])
def getRoutes(req):
    routes = [
        {
            "Endpoint": "/notes/",
            "method": "GET",
            "body": None,
            "description": "Returns an array of notes",
        },
        {
            "Endpoint": "/notes/id",
            "method": "GET",
            "body": None,
            "description": "Returns a single note object",
        },
        {
            "Endpoint": "/notes/create/",
            "method": "POST",
            "body": {"body": ""},
            "description": "Creates new note with data sent in post request",
        },
        {
            "Endpoint": "/notes/id/update/",
            "method": "PUT",
            "body": {"body": ""},
            "description": "Creates an existing note with data sent in post request",
        },
        {
            "Endpoint": "/notes/id/delete/",
            "method": "DELETE",
            "body": None,
            "description": "Deletes and exiting note",
        },
    ]
    return Response(routes)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUsers(req):
    try:
        user = Account.objects.get(username=req.user)
        if not user:
            return Response(responeForm(False, "Not found user!", "error"), status=400)
        return Response(
            responeForm(
                True,
                "Logged in!",
                "success",
                token=None,
                user=AccountSerializer(user).data,
            ),
            status=200,
        )
    except Exception as e:
        print(e)
        return Response(
            {"success": False, "message": "Internal server error"}, status=500
        )


@api_view(["POST"])
def postRegister(req):
    # print("req: ", req.__dict__)
    fullname = req.data["fullname"]
    username = req.data["username"]
    password = req.data["password"]
    repeat = req.data["repeat"]
    email = req.data["email"]
    phone = req.data["phone"]

    if (
        not fullname
        or not username
        or not password
        or not repeat
        or not email
        or not phone
    ):
        return Response(
            {
                "success": False,
                "message": "Missing requested information!",
                "type": "error",
            },
            status=400,
        )
    if password != repeat:
        return Response(
            {"success": False, "message": "Password does not match!", "type": "error"},
            status=400,
        )
    try:
        user = Account.objects.filter(username=username)

        if user:
            return Response(
                {
                    "success": False,
                    "message": "Username already taken!",
                    "type": "error",
                },
                status=400,
            )
        # const hashedPassword = await argon2.hash(password)
        hased = password + "__hased"
        newUser = Account(
            fullname=fullname,
            username=username,
            password=hased,
            email=email,
            phone=phone,
        )
        newUser.save()

        # // Return token
        # // const accessToken = jwt.sign(
        # // 	{ userId: newUser._id },
        # // 	process.env.ACCESS_TOKEN_SECRET
        # // )
        accessToken = "pic2602"
        return Response(
            {
                "success": True,
                "message": "Register successfully!",
                "accessToken": accessToken,
                "type": "success",
            },
            status=200,
        )
    except Exception as e:
        print(e)
        return Response(
            {"success": False, "message": "Internal server error", "type": "error"},
            status=500,
        )


@api_view(["POST"])
def postLogin(req):
    username = req.data["username"]
    password = req.data["password"]

    if not username or not password:
        return Response(
            {
                "success": False,
                "message": "Missing requested information!",
                "type": "error",
            },
            status=400,
        )
    try:
        checkUser = Account.objects.filter(username=username)
        if not checkUser:
            return Response(
                {
                    "success": False,
                    "message": "Username is not exist!",
                    "type": "error",
                },
                status=400,
            )
        existUser = Account.objects.get(username=username)
        if existUser.password != (password + "__hased"):
            return Response(
                {"success": False, "message": "Wrong password!", "type": "error"},
                status=400,
            )
        # const hashedPassword = await argon2.hash(password)

        # // Return token
        # // const accessToken = jwt.sign(
        # // 	{ userId: newUser._id },
        # // 	process.env.ACCESS_TOKEN_SECRET
        # // )
        accessToken = "pic2602"
        return Response(
            {
                "success": True,
                "message": "Login successfully!",
                "accessToken": accessToken,
                "type": "success",
            },
            status=200,
        )
    except Exception as e:
        print(e)
        return Response(
            {"success": False, "message": "Internal server error", "type": "error"},
            status=500,
        )


class UserRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, req):
        fullname = req.data["fullname"]
        username = req.data["username"]
        password = req.data["password"]
        repeat = req.data["repeat"]
        email = req.data["email"]
        phone = req.data["phone"]

        if (
            not fullname
            or not username
            or not password
            or not repeat
            or not email
            or not phone
        ):
            return Response(
                responeForm(False, "Missing requested information!", "warning"),
                status=400,
            )
        if password != repeat:
            return Response(
                responeForm(False, "Password does not match!", "warning"),
                status=400,
            )

        print(req.data)
        serializer = RegisterSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                responeForm(True, "Register successfully!", "success"),
                status=200,
            )
        return Response(
            responeForm(False, serializer.error_messages, "error"), status=400
        )


class UserLoginView(ObtainAuthToken):
    permission_classes = (AllowAny,)

    def post(self, req):
        username = req.data["username"]
        password = req.data["password"]

        if not username or not password:
            return Response(
                responeForm(False, "Missing requested information!", "warning"),
                status=400,
            )
        # serializer = self.get_serializer(data=req.data)
        serializer = LoginSerializer(data=req.data)
        print(serializer)
        if serializer.is_valid():
            print(serializer.validated_data)
            user = authenticate(
                req,
                username=username,
                password=password,
            )
            if user:
                token = Token.objects.get(user=user)
                # refresh = TokenObtainPairSerializer.get_token(user)
                return Response(
                    responeForm(True, "Login successfully!", "success", str(token)),
                    status=200,
                )
            return Response(
                responeForm(False, "Username or password is incorrect!", "error"),
                status=400,
            )

        return Response(responeForm(False, "error", "error"), status=400)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getProducts(req):
    try:
        product = Product.objects.all()

        if not product:
            return Response(
                responeForm(False, "Not found products!", "error"), status=400
            )
        return Response(
            responeForm(
                True,
                "Get products successfully!",
                "success",
                products=ProductSerializer(product, many=True).data,
            ),
            status=200,
        )
    except Exception as e:
        print(e)
        return Response(
            {"success": False, "message": "Internal server error"}, status=500
        )


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getDiscounts(req):
    try:
        discount = DiscountCode.objects.all()

        if not discount:
            return Response(
                responeForm(False, "Not found discount code!", "error"), status=400
            )
        return Response(
            responeForm(
                True,
                "Get discount code successfully!",
                "success",
                discounts=DiscountCodeSerializer(discount, many=True).data,
            ),
            status=200,
        )
    except Exception as e:
        print(e)
        return Response(
            {"success": False, "message": "Internal server error"}, status=500
        )


class Carts(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, req):
        try:
            productId = req.data["productId"]
            product = Product.objects.get(pk=productId)
            cart = Cart(userId=req.user, productId=product, quantity=1)
            cart.save()
            return Response(responeForm(True, "Add into cart successfully", "success"))

        except Exception as e:
            print(e)
            return Response(
                {"success": False, "message": "Internal server error"}, status=500
            )

    def get(self, req):
        try:
            cart = Cart.objects.filter(userId=req.user)
            if not cart:
                return Response(
                    responeForm(False, "Not found products in cart!", "error"),
                    status=400,
                )
            return Response(
                responeForm(
                    True,
                    "Get cart successfully!",
                    "success",
                    cart=CartSerializer(cart, many=True).data,
                ),
                status=200,
            )
        except Exception as e:
            print(e)
            return Response(
                {"success": False, "message": "Internal server error"}, status=500
            )

    def put(self, req):
        try:
            operation = req.data["operation"]
            productId = req.data["productId"]
            product = Product.objects.get(pk=productId)
            cart = Cart.objects.filter(userId=req.user, productId=product).first()
            if not cart:
                return Response(
                    responeForm(False, "This product is not in cart", "error")
                )

            cart.quantity += operation  # 1 if operation == "INC" else -1
            cart.save()
            return Response(responeForm(True, "Update cart successfully", "success"))

        except Exception as e:
            print(e)
            return Response(
                {"success": False, "message": "Internal server error"}, status=500
            )

    def delete(self, req):
        try:
            productId = req.data["productId"]
            product = Product.objects.get(pk=productId)
            cart = Cart.objects.filter(userId=req.user, productId=product)
            if not cart:
                return Response(
                    responeForm(False, "This product is not in cart", "error")
                )
            cart.delete()
            return Response(
                responeForm(True, "Delete into cart successfully", "success")
            )

        except Exception as e:
            print(e)
            return Response(
                {"success": False, "message": "Internal server error"}, status=500
            )


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def getProducts(req):
#     product = req.user.products_owned.all()
#     return Response(ProductSerializer(product, many=True).data)
