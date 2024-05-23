from django.db import transaction
import requests
from django_rest.permissions import IsAuthenticated
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from transactions.models import Balance, Product
from transactions.serializers import ProductSerializer, SendMoneySerializer, BuyProductSerializer, \
    CheckBalanceSerializer
import logging

logger = logging.getLogger('console_logger')


class CheckBalanceAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            balances = Balance.objects.get(user_id=request.user.id)
            return Response({'balance': balances.balance})
        except Exception as e:
            logger.error({
                'message': e,
            })
            return Response({"message": "User does not exists"}, status=status.HTTP_404_NOT_FOUND)


class SendMoneyAPIVIEW(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.data["user"] = request.user.id
        sendMoneySerializer = SendMoneySerializer(data=request.data)
        if sendMoneySerializer.is_valid():
            try:
                receiver_id = request.data.get("id")
                amount = request.data.get("amount")
                receiver_balance_queryset = Balance.objects.filter(user_id=receiver_id).values("balance")
                if receiver_balance_queryset.exists():
                    receiver_old_balance = receiver_balance_queryset[0]['balance']
                    sender_balance = Balance.objects.filter(user_id=request.user.id).values("balance")[0]["balance"]
                    if sender_balance >= amount:
                        with transaction.atomic():
                            Balance.objects.filter(user_id=request.user.id).update(balance=sender_balance - amount)
                            Balance.objects.filter(user_id=receiver_id).update(balance=receiver_old_balance + amount)
                            logger.debug({"Info": f"{request.user} send money to {receiver_id}"})
                            return Response({"Message": "Send Money Successful"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": "Insufficient Balance"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "User doesnt exists"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error({
                    'message': e,
                })
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
            logger.debug(
                f"{request.user} created a product",

            )
            return Response({'message': 'Product created ',
                             'result': {'items': product_serializer.data, }}, status=status.HTTP_201_CREATED)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyProductAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BuyProductSerializer(data=request.data)
        if serializer.is_valid():
            product_id = request.data.get("id")
            product_exist = Product.objects.filter(id=product_id).values_list("owner_id", "stock", "price")
            if product_exist:
                owner, stock, price = product_exist[0]
                quantity = request.data.get("quantity")

                if stock >= quantity and stock >= 0:
                    headers = {
                        'Authorization': request.headers.get('Authorization')
                    }
                    check_balance_queryset = requests.get(" http://localhost:8000/api/check/", headers=headers)
                    balance_data = check_balance_queryset.json()
                    BalanceSerializer = CheckBalanceSerializer(data=balance_data)
                    if BalanceSerializer.is_valid():
                        balance = BalanceSerializer.data.get("balance")
                        owner_balance = Balance.objects.get(user_id=owner)
                        price = quantity * price
                        if price > balance:
                            return Response({'message': "Do not have sufficient balance"},
                                            status=status.HTTP_400_BAD_REQUEST)
                        with transaction.atomic():
                            Balance.objects.filter(user_id=request.user.id).update(balance=balance - price)
                            Balance.objects.filter(user_id=owner).update(balance=owner_balance.balance + price)
                            Product.objects.filter(id=product_id).update(stock=stock - quantity)
                            logger.debug({
                                'info': f"{request.user} bought the product {product_id}",

                            })
                            return Response({'message': "product buying successful"}, status=status.HTTP_200_OK)

                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'stock not available'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'No product found'}, status=status.HTTP_201_CREATED)

        logger.debug(f" Serializer error : {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
