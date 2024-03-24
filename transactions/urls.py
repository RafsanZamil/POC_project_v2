from django.urls import path
from transactions.views import CheckBalanceAPIVIEW, SendAPIVIEW, CreateProductAPIVIEW, BuyProductAPIVIEW

urlpatterns = [
    path("check/", CheckBalanceAPIVIEW.as_view(), name="send_money"),
    path("send/", SendAPIVIEW.as_view(), name="send_money"),
    path("create/product/",CreateProductAPIVIEW.as_view(), name="create_product"),
    path("buy/", BuyProductAPIVIEW.as_view(), name="Buy Product")

]
