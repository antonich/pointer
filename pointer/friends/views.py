from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from friends.serializers import FriendsSerializer
from friends.models import *
from friends.exceptions import *
from users.models import User
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET'])
def friends_list(request):
    if request.user.is_authenticated:
        people = Friendship.objects.friends_list(request.user)
        serializer = FriendsSerializer(people, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def received_requests_list(request):
    if request.user.is_authenticated:
        people = Friendship.objects.request_received_list(request.user)
        serializer = FriendsSerializer(people, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def sent_requests_list(request):
    if request.user.is_authenticated:
        people = Friendship.objects.request_sent_list(request.user)
        serializer = FriendsSerializer(people, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def send_request(request, to_username):
    if request.user.is_authenticated:
        try:
            to_user = User.objects.get(username=to_username)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            Friendship.objects.send_request(request.user, to_user)
        except AlreadyFriendsError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except AlreadyExistsError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=200)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def accept_request(request, pk):
    if request.user.is_authenticated:
        try:
            friendship_request = Request.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        friendship_request.accept()
        return Response(status=200)

    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def decline_request(request, pk):
    if request.user.is_authenticated:
        try:
            friendship_request = Request.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.user.username == friendship_request.from_user.username or \
           request.user.username == friendship_request.to_user.username:
            friendship_request.decline()
            return Response(status=200)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def remove_friendship(request, pk):
    if request.user.is_authenticated:
        try:
            friendship = Friendship.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.user.username == friendship.from_user.username or \
           request.user.username == friendship.to_user.username:
            friendship.delete()
            return Response(status=200)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_401_UNAUTHORIZED)
