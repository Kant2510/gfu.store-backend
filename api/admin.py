from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Product, Account, Cart, DiscountCode

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "sell",
        "price",
        "sale_price",
        "rates",
    ]


class ProductInline(admin.TabularInline):
    model = Cart


class AccountAdmin(UserAdmin):
    list_display = ("id", "username", "email", "phone", "is_active", "is_staff")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("fullname", "email", "phone")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),
    )
    inlines = [
        ProductInline,
    ]
    exclude = ("Products",)
    add_fieldsets = (
        (None, {"fields": ("username", "password1", "password2")}),
        ("Personal info", {"fields": ("fullname", "email", "phone")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


class CartAdmin(admin.ModelAdmin):
    list_display = ["userId", "productId", "quantity"]


class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "discount"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(DiscountCode, DiscountCodeAdmin)


# # admin.site.register(User, UserAdmin)
# admin.site.register(Account, AccountAdmin)
