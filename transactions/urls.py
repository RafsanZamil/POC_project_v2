from django.urls import path
from transactions.views import CheckBalanceAPIVIEW,SendAPIVIEW

urlpatterns = [
    path("check/", CheckBalanceAPIVIEW.as_view(), name="send_money"),
    path("send/", SendAPIVIEW.as_view(), name="send_money"),
]
