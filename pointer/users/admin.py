from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_admin')
    list_filter = ('is_superuser', )

    fieldsets = (
        ('None', {'fields': (
            'username', 'email', 'name', 'password', 'is_superuser', 'is_active' ,'is_admin'
        )}),
        ('Groups', {'fields': ('groups', )})
    )

admin.site.register(User, CustomUserAdmin)
