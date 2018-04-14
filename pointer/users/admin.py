from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import UserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_active', 'is_admin')
    list_filter = ('is_superuser', )

    fieldsets = (
        ('None', {'fields': (
            'username', 'email', 'name', 'password', 'is_superuser', 'is_active' ,'is_admin', 'avatar'
        )}),
        ('Groups', {'fields': ('groups', )})
    )

    add_fieldsets = (
        (None,{
            'classes': ('wide'),
            'fields': ('email', 'username', 'password1', 'password2', 'avatar')
        }),
    )

admin.site.register(User, CustomUserAdmin)
