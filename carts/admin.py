from django.contrib import admin
from .models import CartModel, CartItemsModel

admin.site.register(CartModel)
admin.site.register(CartItemsModel)