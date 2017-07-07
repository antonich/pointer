from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Friendship
from .forms import FriendshipForm

class FriendshipAdmin(admin.ModelAdmin):
    form = FriendshipForm
    list_display = ('from_user', 'to_user',)


admin.site.register(Friendship, FriendshipAdmin)
