from django.urls import path
from transactions.views import CheckBalanceAPIVIEW, SendMoneyAPIVIEW, CreateProductAPIVIEW, BuyProductAPIVIEW

urlpatterns = [
    path("check/", CheckBalanceAPIVIEW.as_view(), name="check_balance"),
    path("send/", SendMoneyAPIVIEW.as_view(), name="send_money"),
    path("create/product/", CreateProductAPIVIEW.as_view(), name="create_product"),
    path("buy/", BuyProductAPIVIEW.as_view(), name="buy_Product")

]
