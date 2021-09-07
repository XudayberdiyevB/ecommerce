from rest_framework import serializers
from .models import CartModel, CartItemsModel


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartModel
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    # cart = CartSerializer()
    class Meta:
        model = CartItemsModel
        fields = '__all__'
