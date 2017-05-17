from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import authenticate, login, logout

from .models import User

VALIDATION_ERROR = 'User is not defined.'

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User.objects.create_user( \
            email=self.validated_data['email'], \
            username=self.validated_data['username'], name=self.validated_data['name'] \
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user
