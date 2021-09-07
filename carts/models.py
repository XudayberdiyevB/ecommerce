from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from products.models import ProductModel
from users.models import User


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user} - {self.total_price}"


class CartItemsModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    price = models.FloatField(default=0, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user) + "-" + str(self.product.name) + "-" + str(self.quantity) + "ta"


@receiver(pre_save, sender=CartItemsModel)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = ProductModel.objects.get(id=cart_items.product.id)
    cart_items.price = float(cart_items.quantity) * float(price_of_product.price)
    # total_cart_items = CartItemsModel.objects.filter(user=cart_items.user)
    # cart = CartModel.objects.get(id=cart_items.cart.id)
    # cart.total_price += cart_items.price
    # cart.save()
