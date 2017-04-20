from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Friendship
from .forms import FriendshipForm

class FriendshipAdmin(admin.ModelAdmin):
    form = FriendshipForm
    list_display = ('userid1', 'userid2',)


admin.site.register(Friendship, FriendshipAdmin)
