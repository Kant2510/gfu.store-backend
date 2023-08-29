from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth.hashers import make_password
from .models import Account, Product, DiscountCode, Cart


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "fullname", "username", "password", "email", "phone")
        extra_kwargs = {"password": {"write_only": True}}


class RegisterSerializer(ModelSerializer):
    """override create method to change the password into hash."""

    class Meta:
        model = Account
        fields = ["fullname", "username", "password", "email", "phone"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(RegisterSerializer, self).create(validated_data)


class LoginSerializer(ModelSerializer):
    username = CharField()

    class Meta:
        model = Account
        fields = ["username", "password"]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ["productId", "quantity"]


class DiscountCodeSerializer(ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = "__all__"
