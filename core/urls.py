from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, UserRetrieveView, UserPasswordUpdateView

urlpatterns = [
    path('signup', UserRegistrationView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', UserRetrieveView.as_view(), name='profile'),
    path('update_password', UserPasswordUpdateView.as_view(), name='update_password')
]
