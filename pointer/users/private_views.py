from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from django.http import Http404
from rest_framework import status, generics, mixins, permissions

from point.models import PrivatePointer
from point.serializers import PrivatePointerSerializer
from members.models import Member
from point.exceptions import *

class CreatePublicPointer(generics.CreateAPIView):
        '''
            Private Pointer creation api view.
        '''
        model = PrivatePointer
        permission_classes = (IsAuthenticated,)
        authentication_classes = (TokenAuthentication, )
        serializer_class = PrivatePointerSerializer
