from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model # for not custom user model

from rest_framework import serializers

from .models import User

VALIDATION_ERROR = 'User is not defined.'


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'name', 'description')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def validate(self, data):
        '''
            Authenticate user
        '''
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("User is not authenticated.")
        else:
            return data

        return data
