from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from point.models import Pointer
from point.serializers import PointerSerializer
from members.models import Member

class PointerList(APIView):
    """
        List user's pointer list.
    """
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, )

    def get_object(self, user):
        try:
            return Member.objects.users_pointer_list(user)
        except Pointer.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        pointer_list = self.get_object(request.user)
        serializer = PointerSerializer(pointer_list, many=True)
        return Response(serializer.data)
