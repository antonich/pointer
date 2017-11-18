from django.conf.urls import url, include

from invite.views import *

urlpatterns = [
    url(r'create_invite/(?P<user_pk>[0-9]+)/(?P<point_pk>[0-9]+)/$', SendInviteView.as_view(), name="create_invite"),
    url(r'accept_invite/(?P<invite_pk>[0-9]+)/$', AcceptInviteView.as_view(), name="accept_invite"),
    url(r'decline_invite/(?P<invite_pk>[0-9]+)/$', DeclineInviteView.as_view(), name="decline_invite"),
    url(r'invite_list/$', InviteListView.as_view(), name="invite_list"),
]
