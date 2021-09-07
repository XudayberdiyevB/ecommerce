import random
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client
from .models import User
from .serializers import RegisterUserSerializer, UserSerializer, ValidationSerializer


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def otp_generate(self):
        otp = random.randint(100000, 999999)
        return otp

    @swagger_auto_schema(request_body=RegisterUserSerializer)
    def post(self, request):
        if self.request.data['phone'] is not None:
            account_sid = "ACd81ae32d0edfa72eece27a981e0cb990"
            auth_token = "a45e9d1782002f73dab76bfcf8341374"
            number = self.request.data['phone']
            client = Client(account_sid, auth_token)
            otp = self.otp_generate()
            body = "Maxfiy kod: " + str(otp)
            message = client.messages.create(from_="+18327531516", body=body, to=number)

            serializer = RegisterUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(email=serializer.validated_data['email'])
                user.code = otp
                user.save()
                return Response(serializer.data)
            return Response(status.HTTP_400_BAD_REQUEST)

        else:
            serializer = RegisterUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permissions_classes = [IsAdminUser]

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(email=request.user.email)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class Validate(APIView):
    @swagger_auto_schema(request_body=ValidationSerializer)
    def put(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        serializer = ValidationSerializer(user, data=request.data)

        if serializer.is_valid():
            code = serializer.validated_data['code']
            if code == user.code:
                user.phone_verify = True
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)