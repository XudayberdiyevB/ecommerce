import random

from carts.models import CartModel
from django.db import models
from users.models import User


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    is_paid = models.BooleanField(default=False)
    order_id = models.IntegerField(default=0, blank=True)
    info = models.TextField()

    payment_choices = (
        ("naqd", "Naqd pulda"),
        ("plastik", "Plastik karta orqali")
    )
    payment_method = models.CharField(max_length=100, choices=payment_choices)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        cart = CartModel.objects.filter(user=self.user)
        self.order_id = random.randint(100000, 1000000)
        super(OrderModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.order_id}"


class OrderedItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.order)
