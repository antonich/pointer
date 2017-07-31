from rest_framework import serializers
from friends.models import Friendship, Request
from users.models import User

class PeopleSerializer(serializers.ModelSerializer):
    """Serialize people"""
    class Meta:
        model = User
        fields = ('id', 'username')

class FriendshipsSerializer(serializers.ModelSerializer):
    """Srialize frienships """
    class Meta:
        model = Friendship
        fields = '__all__'

class RequestsSerializer(serializers.ModelSerializer):
    """Srialize requests """
    class Meta:
        model = Request
        fields = '__all__'
