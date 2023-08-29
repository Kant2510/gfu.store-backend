from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    User,
)
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=True, blank=False)
    publisher = models.TextField(null=True, blank=True)
    version = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=False)
    category = models.TextField(null=True, blank=False)
    os = models.TextField(null=True, blank=True)
    img_url = models.TextField(null=True, blank=False)
    sell = models.TextField(null=True, blank=False)
    price = models.TextField(null=True, blank=False)
    sale = models.TextField(null=True, blank=True)
    sale_price = models.TextField(null=True, blank=True)
    rates = models.IntegerField(null=True, blank=False)
    ori_url = models.URLField(null=True, blank=False)
    youtube = models.URLField(null=True, blank=False)

    def __str__(self):
        return str(self.id)


class CustomUserManager(BaseUserManager):
    def create_user(
        self, username, password, fullname=None, email=None, phone=None, **extra_fields
    ):
        if not username or not password:
            raise ValueError("Miss required information")
        user = self.model(
            username=username,
            password=password,
            email=self.normalize_email(email),
            fullname=fullname,
            phone=phone,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user = self.create_user(username=username, password=password, **extra_fields)
        user.save(using=self._db)
        return user


class Account(AbstractUser):
    # id = models.BigAutoField(primary_key=True)
    fullname = models.TextField(null=True, blank=False)
    username = models.TextField(null=True, blank=False, unique=True)
    password = models.CharField(max_length=20, null=True, blank=False)
    email = models.EmailField(unique=False, null=True, blank=False)
    phone = models.CharField(max_length=15, null=True, blank=False)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    products_owned = models.ManyToManyField(
        to="Product", blank=True, null=True, through="Cart"
    )
    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ["username"]

    # def __str__(self):
    #     return self.email

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    # def has_module_perms(self, app_label):
    #     return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Cart(models.Model):
    userId = models.ForeignKey(Account, on_delete=models.CASCADE)
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True, null=True)


class DiscountCode(models.Model):
    code = models.TextField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
