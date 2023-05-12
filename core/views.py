from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserRetrieveSerializer, UserPasswordUpdateSerializer
from django.contrib.sites import requests
from .models import CustomUser


class UserRegistrationView(CreateAPIView):
    """View для регистрации пользователя"""
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)


class UserLoginView(generics.CreateAPIView):
    """View для аутентификации пользователя"""
    serializer_class = UserLoginSerializer

    def post(self, request: requests, *args: str, **kwargs: int) -> Response:
        serializer: UserLoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user=user)
        return Response({'message': 'User logged in successfully'})


class UserRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """View для изменения профиля пользователя"""
    queryset = CustomUser.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserPasswordUpdateView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserPasswordUpdateSerializer

    def get_object(self) -> CustomUser:
        return self.request.user