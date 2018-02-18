from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model # for not custom user model
from django.conf import settings

from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User

VALIDATION_ERROR = 'User is not defined.'

class UserSerializer(serializers.ModelSerializer):
    """
        Serializer people.
    """
    class Meta:
        model = User
        fields = ('id', 'username')

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'name', 'description')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        print 'siema'
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            # name=validated_data['name'],
        )
        user.set_password(validated_data["password"])
        user.save()
        print user.username
        return user


class SocialSerializer(serializers.Serializer):
    """
        Serializer which accepts an OAuth2 access token.
    """
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )
