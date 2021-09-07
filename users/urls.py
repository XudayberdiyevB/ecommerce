from django.urls import path, include
from .views import RegisterUserView, UserListView, UserDetailView, Validate
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register"),
    path('users/', UserListView.as_view(), name="users"),
    path('users/me/', UserDetailView.as_view(), name="user"),
    path('verify-code/<int:pk>/', Validate.as_view()),
    path('', include(router.urls)),
]