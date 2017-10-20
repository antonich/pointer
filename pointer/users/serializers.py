from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model # for not custom user model

from rest_framework import serializers

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
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

    # def sendEmail(self, datas):
    #         link="http://yourdomain.com/activate/"+datas['activation_key']
    #         c=Context({'activation_link':link,'username':datas['username']})
    #         f = open(MEDIA_ROOT+datas['email_path'], 'r')
    #         t = Template(f.read())
    #         f.close()
    #         message=t.render(c)
    #         #print unicode(message).encode('utf8')
    #         send_mail(datas['email_subject'], message, 'yourdomain <no-reply@yourdomain.com>', [datas['email']], fail_silently=False)
