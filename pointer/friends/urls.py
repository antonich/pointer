from django.conf.urls import url, include
from friends.views import *
from users import views

urlpatterns = [
    url(r'friendslist/$', FriendsList.as_view()),
]