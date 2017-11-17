from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.response import Response

from members.serializers import MemberSerializer
from members.models import Member
from members.choices import *
from point.models import Pointer

class MemberListView(APIView):
    '''
        Members for pointer list api view.
    '''
    model = Member
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    serializer_class = MemberSerializer

    def get_object(self, point_id):
        try:
            point = Pointer.objects.get(pk=point_id)
            return Member.objects.filter(pointer=point)
        except Pointer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        member_list = self.get_object(pk)
        serializer = MemberSerializer(member_list, many=True)
        return Response(serializer.data)

class GoingMemberListView(APIView):
    '''
        Going members for pointer list api view.
    '''
    model = Member
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    serializer_class = MemberSerializer

    def get_object(self, point_id):
        try:
            point = Pointer.objects.get(pk=point_id)
            return Member.objects.filter(pointer=point, status=GOING)
        except Pointer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        member_list = self.get_object(pk)
        serializer = MemberSerializer(member_list, many=True)
        return Response(serializer.data)

class DeclineMemberListView(APIView):
    '''
        Decline members for pointer list api view.
    '''
    model = Member
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
    serializer_class = MemberSerializer

    def get_object(self, point_id):
        try:
            point = Pointer.objects.get(pk=point_id)
            return Member.objects.filter(pointer=point, status=DECLINE)
        except Pointer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        member_list = self.get_object(pk)
        serializer = MemberSerializer(member_list, many=True)
        return Response(serializer.data)
