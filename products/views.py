from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .models import ProductCategoryModel, ProductModel
from .serializers import ProductCategorySerializer, ProductSerializer


# 1.1. Products CRUD + List(filter, sort)
class ProductListView(APIView):

    def get(self, request):
        category = self.request.query_params.get('category')
        pkey = self.request.query_params.get("id")

        if category and pkey:
            queryset = ProductModel.objects.filter(product_category__category=category, id=pkey)
        elif category:
            queryset = ProductModel.objects.filter(product_category__category=category)
        elif pkey:
            queryset = ProductModel.objects.filter(id=pkey)
        else:
            queryset = ProductModel.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get_object(self, pk):
        try:
            return ProductModel.objects.get(pk=pk)
        except ProductModel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = ProductSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        queryset = self.get_object(pk)
        serializer = ProductSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 1.2. Category CRUD + List(filter, sort)
class ProductCategoryListView(APIView):

    def get(self, request):
        category_name = self.request.query_params.get("name")
        pkey = self.request.query_params.get("id")

        if category_name or pkey:
            queryset = ProductCategoryModel.objects.filter(category=category_name, id=id)
        else:
            queryset = ProductCategoryModel.objects.all()
        serializer = ProductCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductCategorySerializer)
    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        invalid_data = {
            'message': 'Kategoriya nomi majburiy maydon'
        }
        return Response(data=invalid_data, status=status.HTTP_400_BAD_REQUEST)


class ProductCategoryDetailView(APIView):
    def get_object(self, pk):
        try:
            return ProductCategoryModel.objects.get(pk=pk)
        except ProductCategoryModel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = ProductCategorySerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        queryset = self.get_object(pk)
        serializer = ProductCategorySerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)