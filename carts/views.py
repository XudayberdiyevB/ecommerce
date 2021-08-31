from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import ProductModel
from .models import CartModel, CartItemsModel
from .serializers import CartItemSerializer


class CartListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = CartModel.objects.filter(user=request.user.id, ordered=False).first()
        queryset = CartItemsModel.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = CartModel.objects.get_or_create(user=user, ordered=False)

        product = ProductModel.objects.get(id=data.get('product'))
        price = product.price
        quantity = data.get('quantity')
        cart_items = CartItemsModel(cart=cart, user=user, product=product, price=price, quantity=quantity)
        cart_items.save()

        total_price = 0
        cart_items = CartItemsModel.objects.filter(user=user, cart=cart.id)
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()

        return Response(status=status.HTTP_201_CREATED)


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CartItemsModel.objects.get(pk=pk)
        except CartItemsModel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = CartItemSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        cart_item = self.get_object(pk)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
