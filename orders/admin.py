from django.contrib import admin
from .models import OrderModel, OrderedItems


class OrderModelAdmin(admin.ModelAdmin):
    class Meta:
        model = OrderModel
        list_filter = ('user', )


admin.site.register(OrderModel, OrderModelAdmin)
admin.site.register(OrderedItems)