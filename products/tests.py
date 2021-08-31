import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from .models import ProductCategoryModel, ProductModel
from .serializers import ProductCategorySerializer, ProductSerializer

client = Client()


# ProductCategoryModel set up
class ProductCategorySetUp(TestCase):
    def setUp(self):
        self.categ_first = ProductCategoryModel.objects.create(category="Kitoblar")
        self.categ_second = ProductCategoryModel.objects.create(category="Maishiy texnikalar")
        self.categ_third = ProductCategoryModel.objects.create(category="Kompyuterlar")

        self.valid_category = {
            'category': 'Kitoblar'
        }

        self.invalid_category = {
            'category': None
        }


# test for ProductCategoryModel
class ProductCategoryModelTest(ProductCategorySetUp):
    def test_category_name(self):
        categ_first = ProductCategoryModel.objects.get(category="Kitoblar")
        categ_second = ProductCategoryModel.objects.get(category="Maishiy texnikalar")
        categ_third = ProductCategoryModel.objects.get(category="Kompyuterlar")

        self.assertEqual(categ_first.category, "Kitoblar")
        self.assertEqual(categ_second.category, "Maishiy texnikalar")
        self.assertEqual(categ_third.category, "Kompyuterlar")


# test for ProductCategory get
class GetAllProductsCategoryTest(ProductCategorySetUp):
    def test_get_all_categories(self):
        response = self.client.get(reverse('categories'))
        categories = ProductCategoryModel.objects.all()
        serializer = ProductCategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# test for ProductCategory create, post
class CreateProductCategoryTest(ProductCategorySetUp):
    def test_create_valid_category(self):
        response = self.client.post(reverse('categories'), data=json.dumps(self.valid_category),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_category(self):
        response = client.post(reverse('categories'), data=(self.invalid_category),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# test for ProductCategory get single
class GetSigleProductCategoryTest(ProductCategorySetUp):
    def test_get_valid_single_category(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': self.categ_first.pk}))
        category = ProductCategoryModel.objects.get(pk=self.categ_first.pk)
        serializer = ProductCategorySerializer(category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_category(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# test for ProductCategory update, put
class UpdateSingleProductCategoryTest(ProductCategorySetUp):
    def test_update_valid_category(self):
        response = self.client.put(reverse('category_detail', kwargs={'pk': self.categ_first.pk}),
                                   data=json.dumps(self.valid_category), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_category(self):
        response = self.client.put(reverse('category_detail', kwargs={'pk': 300}),
                                   data=json.dumps(self.invalid_category), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# test for ProductCategory delete
class DeleteSingleProductCategoryTest(ProductCategorySetUp):
    def test_delete_valid_category(self):
        response = self.client.delete(reverse('category_detail', kwargs={'pk': self.categ_first.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_category(self):
        response = self.client.delete(reverse('category_detail', kwargs={'pk': 500}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ProductModel set up
class ProductSetUp(TestCase):
    def setUp(self):
        self.categ_first = ProductCategoryModel.objects.create(category="Kitoblar")
        self.categ_second = ProductCategoryModel.objects.create(category="Maishiy texnikalar")
        self.categ_third = ProductCategoryModel.objects.create(category="Kompyuterlar")

        self.product1 = ProductModel.objects.create(name="Test name1",
                                                    about_product="test info",
                                                    price=20000,
                                                    status='yangi',
                                                    product_category=self.categ_first
                                                    )

        self.product2 = ProductModel.objects.create(name="Test name2",
                                                    about_product="test info",
                                                    price=40000,
                                                    status='yangi',
                                                    product_category=self.categ_second
                                                    )

        self.valid_product = ProductModel.objects.create(name="Test name3",
                                                         about_product="test info",
                                                         price=30000,
                                                         status='yangi',
                                                         product_category=self.categ_third
                                                         )

        self.invalid_product = ProductModel.objects.create(name="",
                                                           about_product="",
                                                           price=40000,
                                                           status='yangi',
                                                           product_category=self.categ_third
                                                           )


class ProductModelTest(ProductSetUp):
    def test_product_name(self):
        product1 = ProductModel.objects.get(name="Test name1")
        product2 = ProductModel.objects.get(name="Test name2")

        self.assertEqual(product1.name, "Test name1")
        self.assertEqual(product2.name, "Test name2")


# test for Product get
class GetAllProductsTest(ProductSetUp):
    def test_get_all_products(self):
        products = ProductModel.objects.all()
        response = self.client.get(reverse('products'))
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


# test for Product create, post
class CreateProductTest(ProductSetUp):
    def test_create_valid_product(self):
        serializer = ProductSerializer(self.valid_product)
        response = self.client.post(reverse("products"), data=serializer.data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):
        serializer = ProductSerializer(self.invalid_product)
        response = self.client.post(reverse("products"), data=serializer.data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# test for Product get single
class GetSingleProductTest(ProductSetUp):
    def test_get_single_valid_product(self):
        response = self.client.get(reverse("product_detail", kwargs={'pk': self.product1.pk}))
        product = ProductModel.objects.get(pk=self.product1.pk)
        serializer = ProductSerializer(product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_invalid_product(self):
        response = self.client.get(reverse("product_detail", kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# test for Product update, put
class UpdateSingleProductTest(ProductSetUp):
    def test_update_valid_product(self):
        serializer = ProductSerializer(self.valid_product)
        response = self.client.put(reverse("product_detail", kwargs={'pk': self.valid_product.pk}),
                                   data=serializer.data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_product(self):
        serializer = ProductSerializer(self.invalid_product)
        response = self.client.put(reverse("product_detail", kwargs={'pk': self.invalid_product.pk}),
                                   data=serializer.data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# test for delete product
class DeleteSingleProductTest(ProductSetUp):
    def test_delete_valid_product(self):
        response = self.client.delete(reverse('product_detail', kwargs={'pk': self.product1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_product(self):
        response = self.client.delete(reverse('product_detail', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
