from django.contrib import admin
from core.models import CustomUser, CustomUserAdmin

admin.site.register(CustomUser, CustomUserAdmin)