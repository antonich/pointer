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
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

WRONG_PASSWORD = 'The password is wrong.'
UNAUTH_USER = 'This user is not authenticated.'
CONFIRM_EMAIL = 'Check your email to confirm registation.'

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
        Authenticates, logins and creates token!!!
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
                if user.is_active:
                    login(request, user)
                    token = Token.objects.create(user=user)
                    token.save()
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({'errors': CONFIRM_EMAIL}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'errors': UNAUTH_USER},status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    '''
        User logout and deletes token
    '''
    model = get_user_model()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication)

    def post(self, request, format=None):
        token = User.objects.get_user_token(user=request.user)
        token.delete()
        logout(request)

        return Response(status=status.HTTP_200_OK)
