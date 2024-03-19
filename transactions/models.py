from django.db import models
from auths.models import CustomUser


# Create your models here.


class Balance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Balance is {self.balance} Tk "
