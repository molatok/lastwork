from django.urls import path
from .views import UserRegistrationView

urlpatterns = [
    path('core/signup/', UserRegistrationView.as_view(), name='user-registration'),
]
