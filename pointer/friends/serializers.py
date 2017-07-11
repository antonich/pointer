from rest_framework import serializers
from friends.models import Friendship
from users.models import User

class FriendsSerializer(serializers.ModelSerializer):
    """Srialize frienships or requests to frinship list"""
    class Meta:
        model = User
        fields = ('username', 'name')

