
from django.contrib import admin
from .models import Balance, Product


class BalanceAdmin(admin.ModelAdmin):
    list_display = ["user", "get_username", "balance"]
    readonly_fields = []

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'


admin.site.register(Balance, BalanceAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ["owner", "product_name", "price"]
    readonly_fields = []


admin.site.register(Product, ProductAdmin)
