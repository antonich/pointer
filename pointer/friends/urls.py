from django.conf.urls import url, include
from friends.views import *
from users import views

urlpatterns = [
    url(r'friends_list/$', friends_list),
    url(r'received_requests_list/$', received_requests_list),
    url(r'sent_requests_list/$', sent_requests_list),
    url(r'send_request/(?P<to_username>[\w-]+)/$', send_request),
    url(r'accept_request/(?P<from_username>[\w-]+)/$', accept_request),
    url(r'decline_request/(?P<username>[\w-]+)/$', decline_request),
    url(r'remove_friendship/(?P<username>[\w-]+)/$', remove_friendship)
]
