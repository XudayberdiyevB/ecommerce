from django.urls import path, include
from .views import ProductListView, ProductDetailView, ProductCategoryListView, ProductCategoryDetailView


urlpatterns = [
    path('categories/', ProductCategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', ProductCategoryDetailView.as_view(), name='category_detail'),
    path('', ProductListView.as_view(), name='products'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]