from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework import status, generics, mixins, permissions

from point.models import PublicPointer
from point.serializers import PointerSerializer, PublicPointerSerializer
from members.models import Member
from point.exceptions import *

class JoinPublicPointer(APIView):
    """
        How to join pointer.
    """
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, )

    def get_object(self, pk):
        try:
            return PublicPointer.objects.get(pk=pk)
        except PublicPointer.DoesNotExist:
            raise Http404
            # return Response({'errors': PointerDoesNotExist}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        pointer = self.get_object(pk)
        pointer.join(request.user)
        return Response(status=status.HTTP_201_CREATED)

class CreatePublicPointer(generics.CreateAPIView):
        '''
            Public Pointer creation api view.
        '''
        model = PublicPointer
        permission_classes = (IsAuthenticated,)
        #authentication_classes = (TokenAuthentication, )
        serializer_class = PublicPointerSerializer
