from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from friends.serializers import PeopleSerializer
from friends.models import *
from friends.exceptions import *
from users.models import User
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET'])
def friends_list(request):
    if request.user.is_authenticated:
        people = Friendship.objects.friends_list(request.user)
        serializer = PeopleSerializer(people, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def received_requests_list(request):
    if request.user.is_authenticated:
        people = Friendship.objects.request_received_list(request.user)
        serializer = PeopleSerializer(people, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def sent_requests_list(request):
    if request.user.is_authenticated:
        people = Friendship.objects.request_sent_list(request.user)
        serializer = PeopleSerializer(people, many=True)
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
def accept_request(request, from_username):
    if request.user.is_authenticated:
        try:
            friendship_request = Request.objects.get(to_user=request.user,
                                                     from_user=User.objects.get(username=from_username))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        friendship_request.accept()
        return Response(status=200)

    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def decline_request(request, username):
    if request.user.is_authenticated:
        try:
            Request.objects.remove_request(from_user=request.user,
                                           to_user=User.objects.get(username=username))
        except RequestNotFoundError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=200)

    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def remove_friendship(request, username):
    if request.user.is_authenticated:
        try:
            Friendship.objects.remove_friendship(from_user=request.user,
                                                 to_user=User.objects.get(username=username))
        except FriendshipNotFoundError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=200)

    return Response(status=status.HTTP_401_UNAUTHORIZED)
