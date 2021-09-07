from django.db import models


class ProductCategoryModel(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class ProductModel(models.Model):
    product_category = models.ForeignKey(ProductCategoryModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    about_product = models.TextField()
    image = models.FileField(upload_to='img', blank=True, null=True)
    price = models.CharField(max_length=20)
    rating = models.IntegerField(default=0)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"