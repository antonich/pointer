from django.http import Http404
from django.contrib.auth import get_user_model # for not custom user model
from django.contrib.auth import authenticate, login, logout

from .serializers import UserCreationSerializer
from .models import User

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

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
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                token = User.objects.get_user_token(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_400_BAD_REQUEST)
