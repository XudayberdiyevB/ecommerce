from django.urls import path
from .views import CartListView, CartDetailView

urlpatterns = [
    path('', CartListView.as_view(), name="cart_list"),
    path('<int:pk>/', CartDetailView.as_view(), name="cart_detail"),
]