from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import UserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_superuser', 'is_admin')
    list_filter = ('is_superuser', )

    fieldsets = (
        ('None', {'fields': (
            'username', 'email', 'name', 'password', 'is_superuser', 'is_active' ,'is_admin'
        )}),
        ('Groups', {'fields': ('groups', )})
    )

    add_fieldsets = (
        (None,{
            'classes': ('wide'),
            'fields': ('email', 'username', 'password1', 'password2')
        }),
    )

admin.site.register(User, CustomUserAdmin)
