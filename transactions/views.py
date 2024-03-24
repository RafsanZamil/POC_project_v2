from django.db import transaction
import requests
from django_rest.permissions import IsAuthenticated
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from transactions.models import Balance, Product
from transactions.serializers import ProductSerializer, SendMoneySerializer


class CheckBalanceAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            balances = Balance.objects.get(user_id=request.user.id)
            return Response({'balance': balances.balance})
        except Exception as e:
            return Response({"message": f"{e}."}, status=status.HTTP_404_NOT_FOUND)


class SendAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request_data = dict(request.data)
        request_data["user"] = request.user.id
        sender_id = request.user.id
        try:
            receiver_id = request_data.get("id")
            receiver_balance = Balance.objects.get(user_id=receiver_id)
            receiver_old_balance = receiver_balance.balance
            amount = request_data.get("amount")
            sender_balance_queryset = Balance.objects.get(user_id=request.user.id)
            sender_balance = sender_balance_queryset.balance
            sendMoneySerializer = SendMoneySerializer(data=request.data)
            if sendMoneySerializer.is_valid:
                if sender_balance >= amount:
                    Balance.objects.filter(user_id=request.user.id).update(balance=sender_balance - amount)
                    new_bal = Balance.objects.get(user_id=request.user.id)
                    new_bal = new_bal.balance
                    Balance.objects.filter(user_id=receiver_id).update(
                        balance=receiver_old_balance + amount)
                    receivers_new_balance = Balance.objects.get(user_id=receiver_id).balance
                    response = {
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
            else:
                return Response(SendMoneySerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"{e}."}, status=status.HTTP_404_NOT_FOUND)


class CreateProductAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_data = dict(request.data)
        request_data["owner"] = request.user.id
        product_serializer = ProductSerializer(data=request_data)
        if product_serializer.is_valid():
            product_serializer.save()

            return Response({'message': 'Product created ',
                             'result': {'items': product_serializer.data, }}, status=status.HTTP_201_CREATED)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyProductAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        with transaction.atomic():
            print(request.headers)
            request_data = dict(request.data)
            product_id = request_data.get("id")
            owner = Product.objects.get(id=product_id)
            owner = owner.owner_id
            items = request_data.get("items")
            product_exist = Product.objects.filter(id=product_id)
            if product_exist:
                stock = Product.objects.get(id=product_id)
                stock = stock.stock
                price = Product.objects.get(id=product_id).price
                if stock >= items and stock >= 0:
                    price = items * price
                    headers = {
                        'Authorization': request.headers.get('Authorization')
                    }
                    check_bal = requests.get(" http://localhost:8000/api/check/", headers=headers)
                    check_bal = check_bal.json().get("balance")
                    owner_bal = Balance.objects.get(user_id=owner)

                    if price > check_bal:
                        return Response({'message': "Do not have sufficient balance"})

                    Balance.objects.filter(user_id=request.user.id).update(balance=check_bal - price)
                    Balance.objects.filter(user_id=owner).update(balance=owner_bal.balance + price)
                    Product.objects.filter(id=product_id).update(stock=stock - items)

                    return Response({'message': "you bought the product"})
                else:
                    return Response({'message': 'stock not available'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'No product found'}, status=status.HTTP_201_CREATED)
