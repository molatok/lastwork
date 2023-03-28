from django.contrib import admin
from core.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    readonly_fields = ('last_login', 'date_joined',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exclude = ('password',)


admin.site.register(CustomUser, CustomUserAdmin)
