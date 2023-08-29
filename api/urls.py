from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("auth/", views.getUsers, name="users"),
    path("auth/register", views.UserRegisterView.as_view(), name="register"),
    path("auth/login", views.UserLoginView.as_view(), name="login"),
    path("cart/", views.Carts.as_view(), name="cart"),
    path("products/", views.getProducts, name="products"),
    path("discounts/", views.getDiscounts, name="discounts"),
]
