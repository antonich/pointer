from django.http import Http404
from django.contrib.auth import get_user_model # for not custom user model

from .serializers import UserCreationSerializer, UserLoginSerializer
from .models import User

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins, permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.


'''
    API Views
'''
class UserCreationView(generics.CreateAPIView):
    '''
        User creation api view
    '''
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Everyone has access
    ]
    serializer_class = UserCreationSerializer


class UserLoginView(APIView):
    '''
        User login view
    '''
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Everyone has access
    ]

    def post(self, request, format=None):
        if not request.user.is_anonymous():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserLoginSerializer(data=request.data)
            try:
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)#, {'Token': 'token'})
                print serializer.errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except:
                pass

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
