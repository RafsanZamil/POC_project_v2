from django.db import transaction
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import Balance


# Create your views here.
class CheckBalanceAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        balances = Balance.objects.get(user_id=request.user.id)

        return HttpResponse(f"Your balance is {balances.balance} Tk")


class SendAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        with transaction.atomic():

            request_data = dict(request.data)
            sender_id = request.user.id
            receiver_id = request_data.get("id")
            receiver_balance = Balance.objects.get(user_id=receiver_id)
            receiver_old_balance = receiver_balance.balance
            amount = request_data.get("amount")
            sender_balance_queryset = Balance.objects.get(user_id=request.user.id)
            sender_balance = sender_balance_queryset.balance
            if sender_balance >= amount:
                Balance.objects.filter(user_id=request.user.id).update(balance=sender_balance - amount)
                new_bal = Balance.objects.get(user_id=request.user.id)
                new_bal = new_bal.balance
                receiver_balance = Balance.objects.filter(user_id=receiver_id).update(balance=receiver_old_balance + amount)
                receivers_new_balance = Balance.objects.get(user_id=receiver_id).balance
                response={
                    "sender's_id": sender_id,
                    "receiver's_id": receiver_id,
                    "receiver's_balance": receiver_old_balance,
                    "receiver's_new_balance": receivers_new_balance,
                    "sender_balance": sender_balance,
                    "sender's_new_balance": new_bal
                }

                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Insufficient Balance"}, status=status.HTTP_400_BAD_REQUEST)



