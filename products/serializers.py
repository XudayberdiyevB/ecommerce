from rest_framework import serializers

from .models import ProductCategoryModel, ProductModel


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryModel
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"
