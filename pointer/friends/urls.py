from django.conf.urls import url, include
from friends.views import *
from users import views

urlpatterns = [
    url(r'friends_list/$', FriendsList.as_view()),
    url(r'received_requests_list/$', ReceivedRequestsList.as_view()),
    url(r'sent_requests_list/$', SentRequestsList.as_view()),
    url(r'send_request/(?P<pk>[0-9]+)/$', SendRequest.as_view()),
    url(r'accept_request/(?P<pk>[0-9]+)/$', AcceptRequest.as_view()),
    url(r'decline_request/(?P<pk>[0-9]+)/$', DeclineRequest.as_view()),
    url(r'remove_friendship/(?P<pk>[0-9]+)/$', RemoveFriendship.as_view())
]
