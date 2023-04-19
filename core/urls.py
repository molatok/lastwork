from django.urls import path
from .views import UserRegistrationView

urlpatterns = [
    path('core/sign-up/', UserRegistrationView.as_view(), name='user-registration'),
]
