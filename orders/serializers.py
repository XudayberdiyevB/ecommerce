from rest_framework import serializers

from .models import OrderModel, OrderedItems


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = '__all__'


class OrderedItemSerializer(serializers.ModelSerializer):
    # user = User()
    # order = OrderModel()
    class Meta:
        model = OrderedItems
        fields = '__all__'
