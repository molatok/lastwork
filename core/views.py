from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer


class UserRegistrationView(CreateAPIView):
    """View для регистрации пользователя"""
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, uwer=user)
        return Response(serializer.data)



