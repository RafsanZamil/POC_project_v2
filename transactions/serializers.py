from rest_framework import serializers

from transactions.models import Product, Balance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_stock(self, value):
        if value < 1:
            raise serializers.ValidationError('Stock has to be more than 1')
        return value


class BuyProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class CheckBalanceSerializer(serializers.Serializer):
    balance = serializers.IntegerField()


class SendMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'
