from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.sites import requests


class UserRegistrationView(CreateAPIView):
    """View для регистрации пользователя"""
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request: requests, *args: str, **kwargs: int) -> Response:
        serializer: UserLoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user=user)
        return Response({'message': 'User logged in successfully'})

