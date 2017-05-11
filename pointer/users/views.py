from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import viewsets

from .serializers import UserSerializer, GroupSerializer
from .models import User

# Create your views here.


'''
    API Views
'''

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
