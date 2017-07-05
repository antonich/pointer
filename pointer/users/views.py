from django.http import Http404
from django.contrib.auth import get_user_model # for not custom user model

from .serializers import UserCreationSerializer
from .models import User

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins, permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.


'''
    API Views
'''
class UserCreationView(generics.CreateAPIView):
    '''
        Info about user is logged and form for registation if not
    '''
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserCreationSerializer

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
