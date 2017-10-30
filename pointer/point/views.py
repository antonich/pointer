from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from point.models import Pointer
from point.serializers import PointerSerializer
from members.models import Member

class AuthorPointerList(APIView):
    """
        Author pointer list.
    """
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, )

    def get(self, request, format=None):
        pointer_list = Pointer.objects.author_pointer_list(request.user)
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
