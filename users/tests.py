from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User
from .serializers import UserSerializer


class UserSetUp(APITestCase):
    def setUp(self):
        # self.register_url = reverse('register')
        # self.login_url = reverse('token_obtain_pair')
        faker = Faker()

        self.email1 = faker.email()
        self.password1 = faker.password()

        self.email2 = faker.email()
        self.password2 = faker.password()
        self.first_name2 = faker.first_name()
        self.last_name2 = faker.last_name()
        self.phone2 = faker.phone_number()

        self.user1 = User.objects.create_user(email=self.email1, password=self.password1)
        self.user2 = User.objects.create(email=self.email2,
                                         password=self.password2,
                                         first_name=self.first_name2,
                                         last_name=self.last_name2)

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class UserListTest(UserSetUp):
    def test_get_users(self):
        self.user2.is_admin = True
        self.user2.save()
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(reverse("users"))
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)


class DetailUserTest(UserSetUp):
    def test_detail_user(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(reverse("user"))
        user = User.objects.get(email=self.user2.email)
        serializer = UserSerializer(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data, serializer.data)