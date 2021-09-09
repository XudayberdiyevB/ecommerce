from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated

from carts.models import CartModel
from .models import OrderModel, OrderedItems
from .serializers import OrderSerializers, OrderedItemSerializer


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = OrderModel.objects.filter(user=request.user)
        serializer = OrderSerializers(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        queryset = OrderModel.objects.all()
        queryset.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class OrderedItemListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = OrderedItems.objects.filter(user=request.user)
        serializer = OrderedItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderedItemSerializer(data=request.data)
        cart = CartModel.objects.get(self.request.user)
        if serializer.is_valid():
            serializer.save()
            cart.ordered = True
            cart.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)