import json

from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from carts.models import CartModel, CartItemsModel
from orders.models import OrderModel, OrderedItems
from orders.serializers import OrderSerializers, OrderedItemSerializer
from products.models import ProductCategoryModel, ProductModel
from users.models import User


class OrderModelSetUp(APITestCase):
    def setUp(self):
        faker = Faker()
        self.email = faker.email()
        self.password = faker.password()
        self.first_name = faker.first_name()
        self.last_name = faker.last_name()
        self.user = User.objects.create(email=self.email,
                                        password=self.password,
                                        first_name=self.first_name,
                                        last_name=self.last_name
                                        )

        self.cart = CartModel.objects.create(user=self.user)

        self.categ_product = ProductCategoryModel.objects.create(category="Kitoblar")

        self.product1 = ProductModel.objects.create(name="Test name1",
                                                    about_product="test info",
                                                    price=20000,
                                                    status="yangi",
                                                    product_category=self.categ_product
                                                    )

        self.cart_item = CartItemsModel.objects.create(cart=self.cart,
                                                       user=self.user,
                                                       product=self.product1,
                                                       price=30000,
                                                       quantity=3)

        self.order_product = OrderModel.objects.create(user=self.user,
                                                       cart=self.cart,
                                                       info="Info",
                                                       payment_method="naqd")

        self.ordered_item = OrderedItems.objects.create(user=self.user, order=self.order_product)


class OrderModelTest(OrderModelSetUp):
    def test_create_order(self):
        order = OrderModel.objects.get(user=self.user)
        self.assertEqual(order.user, self.user)


class GetAllOrderTest(OrderModelSetUp):
    def test_get_all_order(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("order_list"))
        order = OrderModel.objects.filter(user=self.user)
        serializer = OrderSerializers(order, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class CreateOrderTest(OrderModelSetUp):
    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        serializer = OrderSerializers(self.order_product)
        response = self.client.post(reverse("order_list"), data=json.dumps(serializer.data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetOrderedItemsTest(OrderModelSetUp):
    def test_get_ordered_items(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("ordered_items"))
        ordered_items = OrderedItems.objects.filter(user=self.user)
        serializer = OrderedItemSerializer(ordered_items, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class CreateOrderedItemsTest(OrderModelSetUp):
    def test_create_ordered_items(self):
        self.client.force_authenticate(user=self.user)
        serializer = OrderedItemSerializer(self.ordered_item)
        response = self.client.post(reverse("ordered_items"), data=json.dumps(serializer.data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
