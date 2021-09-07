from django.urls import path
from .views import OrderListView, OrderedItemListView

urlpatterns = [
    path('', OrderListView.as_view(), name="order_list"),
    path('done/', OrderedItemListView.as_view(), name="ordered_items"),
]