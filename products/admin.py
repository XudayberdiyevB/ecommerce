from django.contrib import admin
from .models import ProductCategoryModel, ProductModel

admin.site.register(ProductCategoryModel)
admin.site.register(ProductModel)