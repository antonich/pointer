from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, generics, mixins, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer


from users.serializers import UserSerializer
from friends.models import *
from friends.exceptions import *
from users.models import User


NO_SUCH_OBJECT = 'Such type dont exist.'

# @api_view(['GET'])
# def friends_list(request):
#     if request.user.is_authenticated:
#         people = Friendship.objects.friends_list(request.user)
#         serializer = PeopleSerializer(people, many=True)
#         return Response(serializer.data)
#     else:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

class FriendsList(APIView):
    """
    List all friends of request user.
    """
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, )

    def get(self, request, format=None):
        people = Friendship.objects.friends_list(request.user)
        serializer = UserSerializer(people, many=True)
        return Response(serializer.data)
#
# @api_view(['GET'])
# def received_requests_list(request):
#     if request.user.is_authenticated:
#         people = Friendship.objects.request_received_list(request.user)
#         serializer = PeopleSerializer(people, many=True)
#         return Response(serializer.data)
#     else:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

class ReceivedRequestsList(APIView):
    """
        List all friend's requests.
    """
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, )

    def get(self, request, format=None):
        requests = Request.objects.users_received_requests(request.user)
        serializer = UserSerializer(requests, many=True)
        return Response(serializer.data)


# @api_view(['GET'])
# def sent_requests_list(request):
#     if request.user.is_authenticated:
#         people = Friendship.objects.request_sent_list(request.user)
#         serializer = PeopleSerializer(people, many=True)
#         return Response(serializer.data)
#     else:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

class SentRequestsList(APIView):
    """
        List all requested user friendship requests sent.
    """
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, )

    def get(self, request, format=None):
        people = Request.objects.users_sent_requests(request.user)
        serializer = UserSerializer(people, many=True)
        return Response(serializer.data)


# @api_view(['POST'])
# def send_request(request, to_username):
#     if request.user.is_authenticated:
#         try:
#             to_user = User.objects.get(username=to_username)
#         except ObjectDoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         try:
#             Friendship.objects.send_request(request.user, to_user)
#         except AlreadyFriendsError:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         except AlreadyExistsError:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         except ValidationError:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         return Response(status=200)
#     else:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

class SendRequest(APIView):
    """
        Send friendship request.
    """
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, )

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404({'detail':NO_SUCH_OBJECT})
            # return Response(data={'detail':NO_SUCH_OBJECT},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        to_user = self.get_object(pk)

        try:
            Request.objects.send_request(request.user, to_user)
        except AlreadyFriendsError:
            return Response(data={'detail':ALREADY_FRIENDS_ERROR},status=status.HTTP_400_BAD_REQUEST)
        except AlreadyExistsError:
            return Response(data={'detail':ALREADY_EXISTS_ERROR}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response(data={'detail':SAME_USER_ERROR}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# def accept_request(request, from_username):
#     if request.user.is_authenticated:
#         try:
#             friendship_request = Request.objects.get(to_user=request.user,
#                                                      from_user=User.objects.get(username=from_username))
#         except ObjectDoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         friendship_request.accept()
#         return Response(status=200)
#
#     return Response(status=status.HTTP_401_UNAUTHORIZED)

class AcceptRequest(APIView):
    """
        Accept friendship request.
    """
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, )

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404({'detail':NO_SUCH_OBJECT})
            # return Response(data={'detail':NO_SUCH_OBJECT},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        user = self.get_object(pk)
        try:
            friendship_request = Request.objects.get(to_user=request.user, \
                                                     from_user=User.objects.get(username=user.username))
        except ObjectDoesNotExist:
            return Response(data={'detail': NO_SUCH_OBJECT}, status=status.HTTP_400_BAD_REQUEST)

        friendship_request.accept()
        return Response(status=status.HTTP_200_OK)


#
# @api_view(['POST'])
# def decline_request(request, username):
#     if request.user.is_authenticated:
#         try:
#             Request.objects.remove_request(from_user=request.user,
#                                            to_user=User.objects.get(username=username))
#         except RequestNotFoundError:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=200)
#
#     return Response(status=status.HTTP_401_UNAUTHORIZED)

class DeclineRequest(APIView):
    """
        Decline friendship request.
    """
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, )

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404({'detail':NO_SUCH_OBJECT})
            # return Response(data={'detail':NO_SUCH_OBJECT},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        user = self.get_object(pk)
        try:
            Request.objects.remove_request(from_user=request.user,
                                           to_user=User.objects.get(username=user.username))
        except RequestNotFoundError:
            return Response(data={'detail': NO_SUCH_OBJECT}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

# @api_view(['POST'])
# def remove_friendship(request, username):
#     if request.user.is_authenticated:
#         try:
#             Friendship.objects.remove_friendship(from_user=request.user,
#                                                  to_user=User.objects.get(username=username))
#         except FriendshipNotFoundError:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=200)
#
#     return Response(status=status.HTTP_401_UNAUTHORIZED)

class RemoveFriendship(APIView):
    """
        Remove friendship request.
    """
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, )

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404({'detail':NO_SUCH_OBJECT})
            # return Response(data={'detail':NO_SUCH_OBJECT},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        user = self.get_object(pk)
        try:
            Friendship.objects.remove_friendship(from_user=request.user,
                                                 to_user=User.objects.get(username=user.username))
        except FriendshipNotFoundError:
            return Response(data={'detail': NO_SUCH_OBJECT}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
