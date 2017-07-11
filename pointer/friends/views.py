from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from friends.serializers import FriendsSerializer
from friends.models import *
# Create your views here.
import users

class FriendsList(APIView):
    """List of all users friends"""

    def post(self, request, format=None):
        user = users.models.User.objects.get(username=request.data['username'])
        friends = FriendshipManager.friends_list(user)

        serializer = FriendsSerializer(friends, many=True)
        return Response(serializer.data)
