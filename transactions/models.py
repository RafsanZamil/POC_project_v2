from django.db import models
from auths.models import CustomUser


class Balance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, blank=True,decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Balance of {self.user} is {self.balance} Tk "


class Product(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, unique=True)
    stock = models.IntegerField()
    price = models.DecimalField(decimal_places=2,max_digits=10)

    def __str__(self):
        return f"product {self.id} has {self.stock}  stock"
