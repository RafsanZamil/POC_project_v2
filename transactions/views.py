from django.db import transaction
import requests
from django_rest.permissions import IsAuthenticated
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from transactions.models import Balance, Product
from transactions.serializers import ProductSerializer, SendMoneySerializer, BuyProductSerializer, \
    CheckBalanceSerializer


class CheckBalanceAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            balances = Balance.objects.get(user_id=request.user.id)
            return Response({'balance': balances.balance})
        except Exception as e:
            return Response({"message": "User does not exists"}, status=status.HTTP_404_NOT_FOUND)


class SendMoneyAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.data["user"] = request.user.id
        sendMoneySerializer = SendMoneySerializer(data=request.data)
        if sendMoneySerializer.is_valid:
            try:
                receiver_id = request.data.get("id")
                amount = request.data.get("amount")
                receiver_balance_queryset = Balance.objects.filter(user_id=receiver_id).values("balance")
                receiver_old_balance = receiver_balance_queryset[0]['balance']
                sender_balance_queryset = Balance.objects.filter(user_id=request.user.id).values("balance")
                sender_old_balance = sender_balance_queryset[0]['balance']
                if sender_old_balance >= amount:
                    with transaction.atomic():
                        Balance.objects.filter(user_id=request.user.id).update(balance=sender_old_balance - amount)
                        Balance.objects.filter(user_id=receiver_id).update(balance=receiver_old_balance + amount)

                        return Response({"Message": "Send Money Successful"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Insufficient Balance"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"message": f"{e}."}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(SendMoneySerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateProductAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data["owner"] = request.user.id
        product_serializer = ProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()

            return Response({'message': 'Product created ',
                             'result': {'items': product_serializer.data, }}, status=status.HTTP_201_CREATED)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyProductAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BuyProductSerializer(data=request.data)
        if serializer.is_valid():
            product_id = request.data.get("id")
            product_exist = Product.objects.filter(id=product_id)
            if product_exist:
                product_queryset = Product.objects.filter(id=product_id).values_list("owner_id", "stock", "price")
                owner, stock, price = product_queryset[0]
                quantity = request.data.get("quantity")

                if stock >= quantity and stock >= 0:
                    price = quantity * price
                    headers = {
                        'Authorization': request.headers.get('Authorization')
                    }
                    check_balance_queryset = requests.get(" http://localhost:8000/api/check/", headers=headers)
                    balance_data = check_balance_queryset.json()
                    serializer = CheckBalanceSerializer(data=balance_data)
                    if serializer.is_valid():
                        balance = serializer.data.get("balance")
                        owner_balance = Balance.objects.get(user_id=owner)

                        if price > balance:
                            return Response({'message': "Do not have sufficient balance"},
                                            status=status.HTTP_400_BAD_REQUEST)
                        with transaction.atomic():
                            Balance.objects.filter(user_id=request.user.id).update(balance=balance - price)
                            Balance.objects.filter(user_id=owner).update(balance=owner_balance.balance + price)
                            Product.objects.filter(id=product_id).update(stock=stock - quantity)
                            return Response({'message': "you bought the product"}, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'stock not available'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'No product found'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
