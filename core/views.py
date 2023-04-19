from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer


class UserRegistrationView(CreateAPIView):
    """View для регистрации пользователя"""
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
