from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import viewsets

from .serializers import UserSerializer, GroupSerializer
from .models import User

# Create your views here.


'''
    API Views
'''
# class 
