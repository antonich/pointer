from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication

from point.models import Pointer
from point.serializers import PointerSerializer
from members.models import Member
from users.models import User

class UserPointerStory(APIView):
    """
        Author pointer list.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def get_object(self, request_user):
        try:
            user = User.objects.get(pk=request_user.pk)
            return Pointer.objects.get_suggested_pointerlist(user)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        pointer_list = self.get_object(request.user)
        serializer = PointerSerializer(pointer_list, many=True)
        return Response(serializer.data)


class AuthorPointerList(APIView):
    """
        Author pointer list.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def get_object(self, request_user):
        try:
            user = User.objects.get(pk=request_user.pk)
            return Pointer.objects.author_pointer_list(user)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        pointer_list = self.get_object(request.user)
        serializer = PointerSerializer(pointer_list, many=True)
        return Response(serializer.data)

class CreatePointer(APIView):
    '''
        Pointer creation api view.
    '''
    model = Pointer
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, )
    serializer_class = PointerSerializer

class DeletePointer(APIView):
    '''
        Pointer delete api view.
    '''
    model = Pointer
    authentication_classes = (TokenAuthentication, )
    serializer_class = PointerSerializer

    def get_object(self, pk):
        try:
            return Pointer.objects.get(pk=pk)
        except Pointer.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        pointer = self.get_object(pk)
        pointer.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
