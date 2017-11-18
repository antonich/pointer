from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.response import Response
from rest_framework import status, generics, mixins, permissions

from users.models import User
from invite.models import Invite
from invite.serializers import InviteSerializer
from friends.models import Friendship
from point.models import PrivatePointer
from point.exceptions import *

class InviteListView(APIView):
    '''
        List invite list for user.
    '''
    model = Invite
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    serializer_class = InviteSerializer

    def get_object(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return Invite.objects.filter(to_user=user)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        invite_list = self.get_object(request.user.id)
        serializer = InviteSerializer(invite_list, many=True)
        return Response(serializer.data)

class SendInviteView(APIView):
    '''
        Send invite to user.
    '''
    model = Invite
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    serializer_class = InviteSerializer

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

    def get_point(self, point_id):
        try:
            return PrivatePointer.objects.get(id=point_id)
        except PrivatePointer.DoesNotExist:
            raise Http404

    def put(self, request, user_pk, point_pk, format=None):
        to_user = self.get_user(user_pk)
        point = self.get_point(point_pk)
        serial = InviteSerializer(data={'to_user': to_user.pk, 'pointer': point.pk})
        serial.is_valid()
        serial.save()
        return Response(status=status.HTTP_201_CREATED)

class AcceptInviteView(APIView):
    '''
        Accept invite to user and create private pointer.
    '''
    model = Invite
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    serializer_class = InviteSerializer

    def get_invite(self, invite_id, user_id):
        try:
            to_user = User.objects.get(id=user_id)
            return Invite.objects.get(id=invite_id, to_user=to_user)
        except Invite.DoesNotExist:
            raise Http404
        except User.DoesNotExist:
            raise Http404

    def put(self, request, invite_pk, format=None):
        invite = self.get_invite(invite_pk, request.user.pk)
        invite.accept()
        return Response(status=status.HTTP_202_ACCEPTED)

class DeclineInviteView(APIView):
    '''
        Accept invite to user and create private pointer.
    '''
    model = Invite
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    serializer_class = InviteSerializer

    def get_invite(self, invite_id, user_id):
        try:
            to_user = User.objects.get(id=user_id)
            return Invite.objects.get(id=invite_id, to_user=to_user)
        except Invite.DoesNotExist:
            raise Http404
        except User.DoesNotExist:
            raise Http404

    def put(self, request, invite_pk, format=None):
        invite = self.get_invite(invite_pk, request.user.pk)
        invite.decline()

        return Response(status=status.HTTP_202_ACCEPTED)
