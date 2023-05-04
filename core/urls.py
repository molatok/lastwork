from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserRetrieveView

urlpatterns = [
    path('signup', UserRegistrationView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', UserRetrieveView.as_view(), name='profile'),
]
