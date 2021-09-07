import json

from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import ProductCategoryModel, ProductModel
from users.models import User
from .models import CartModel, CartItemsModel
from .serializers import CartItemSerializer


class CartSetUp(APITestCase):
    def setUp(self):
        faker = Faker()
        self.email = faker.email()
        self.password = faker.password()
        self.user = User.objects.create_user(email=self.email,
                                             password=self.password,
                                             )

        self.cart = CartModel.objects.create(user=self.user)


class CartModelTest(CartSetUp):
    def test_cart_user(self):
        cart = CartModel.objects.get(user=self.user)
        self.assertEqual(cart.user, self.user)


class CartItemsSetup(APITestCase):
    def setUp(self):
        faker = Faker()
        self.email = faker.email()
        self.password = faker.password()
        self.user = User.objects.create_user(email=self.email,
                                             password=self.password,
                                             )

        self.cart = CartModel.objects.create(user=self.user)

        self.categ_product = ProductCategoryModel.objects.create(category="Kitoblar")

        self.product1 = ProductModel.objects.create(name="Test name1",
                                                    about_product="test info",
                                                    price=20000,
                                                    status="yangi",
                                                    product_category=self.categ_product
                                                    )

        self.valid_cart_item = CartItemsModel.objects.create(cart=self.cart,
                                                             user=self.user,
                                                             product=self.product1,
                                                             price=30000,
                                                             quantity=3)

        self.invalid_cart_item = CartItemsModel.objects.create(cart=self.cart,
                                                               user=self.user,
                                                               product=self.product1,
                                                               price=None,
                                                               quantity=3)


class CartItemsModelTest(CartItemsSetup):
    def test_cart_items(self):
        cart_item = CartItemsModel.objects.filter(cart__user=self.user).first()
        self.assertEqual(cart_item.cart, self.cart)


class GetAllCartItemsTest(CartItemsSetup):
    def test_get_all_cart(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('cart_list'))
        cart = CartItemsModel.objects.filter(cart__user=self.user, cart__ordered=False)
        serializer = CartItemSerializer(cart, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class CreateCartItemsTest(CartItemsSetup):
    def test_create_cart_test(self):
        self.client.force_authenticate(user=self.user)
        serializer = CartItemSerializer(self.valid_cart_item)
        response = self.client.post(reverse('cart_list'), data=json.dumps(serializer.data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetSingleCartItemsTest(CartItemsSetup):
    def test_get_single_valid_cart_item(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('cart_detail', kwargs={'pk': self.valid_cart_item.pk}))
        cart_items = CartItemsModel.objects.get(pk=self.valid_cart_item.pk)
        serializer = CartItemSerializer(cart_items)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_invalid_cart_item(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('cart_detail', kwargs={'pk': 300}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleCartItemsTest(CartItemsSetup):
    def test_update_cart_items(self):
        self.client.force_authenticate(user=self.user)
        serializer = CartItemSerializer(self.valid_cart_item)
        response = self.client.put(reverse("cart_detail", kwargs={'pk': self.valid_cart_item.pk}),
                                   data=json.dumps(serializer.data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteSingleCartItemsTest(CartItemsSetup):
    def test_delete_single_valid_cart_items(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("cart_detail", kwargs={'pk': self.valid_cart_item.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
