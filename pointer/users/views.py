from django.http import Http404
from django.contrib.auth import get_user_model # for not custom user model
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.views.decorators.http import require_http_methods

from .serializers import UserCreationSerializer, SocialSerializer
from .models import User

from rest_framework import viewsets
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes

from requests.exceptions import HTTPError

from social_django.utils import psa
from social_django.models import UserSocialAuth


WRONG_PASSWORD = 'The password is wrong.'
UNAUTH_USER = 'This user is not authenticated.'
CONFIRM_EMAIL = 'Check your email to confirm registation.'
TOKEN_ALREADY_GEN = 'Token already generated.'


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
    authentication_classes = (BasicAuthentication, )

    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    token = Token.objects.create(user=user)
                    token.save()
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                except:
                    return Response({'detail': TOKEN_ALREADY_GEN}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': CONFIRM_EMAIL}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': UNAUTH_USER},status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    '''
        User logout and deletes token
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def post(self, request, format=None):
        try:
            token = User.objects.get_user_token(user=request.user)
            token.delete()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        logout(request)

        return Response(status=status.HTTP_200_OK)

class UserActivationView(APIView):
    '''
        User needs to activate account though email to be able to login
    '''
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request, key, format=None):
        user = User.objects.get(activation_key=key)
        user.is_active = True
        user.save()

        return Response(status=status.HTTP_200_OK)

class CheckIfTokenIsActive(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def get(self, request, format=None):
        return Response({'detail': "Key is active"}, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@permission_classes([permissions.AllowAny])
@psa()
def exchange_token(request, backend):
    """
    Exchange an OAuth2 access token for one for this site.
    This simply defers the entire OAuth2 process to the front end.
    The front end becomes responsible for handling the entirety of the
    OAuth2 process; we just step in at the end and use the access token
    to populate some user identity.
    The URL at which this view lives must include a backend field, like:
        url(API_ROOT + r'social/(?P<backend>[^/]+)/$', exchange_token),
    Using that example, you could call this endpoint using i.e.
        POST API_ROOT + 'social/facebook/'
        POST API_ROOT + 'social/google-oauth2/'
    Note that those endpoint examples are verbatim according to the
    PSA backends which we configured in settings.py. If you wish to enable
    other social authentication backends, they'll get their own endpoints
    automatically according to PSA.
    ## Request format
    Requests must include the following field
    - `access_token`: The OAuth2 access token provided by the provider
    """
    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # set up non-field errors key
        # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'

        try:
            # this line, plus the psa decorator above, are all that's necessary to
            # get and populate a user object for any properly enabled/configured backend
            # which python-social-auth can handle.
            user = request.backend.do_auth(serializer.validated_data['access_token'])

            # making user automatically active
            user.is_active = True
            user.save()
        except HTTPError as e:
            # An HTTPError bubbled up from the request to the social auth provider.
            # This happens, at least in Google's case, every time you send a malformed
            # or incorrect access key.
            return Response(
                {'errors': {
                    'token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            if user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                # user is not active; at some point they deleted their account,
                # or were banned by a superuser. They can't just log in with their
                # normal credentials anymore, so they can't log in with social
                # credentials either.
                return Response(
                    {'errors': {nfe: 'This user account is inactive'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Unfortunately, PSA swallows any information the backend provider
            # generated as to why specifically the authentication failed;
            # this makes it tough to debug except by examining the server logs.
            return Response(
                {'errors': {nfe: "Authentication Failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
