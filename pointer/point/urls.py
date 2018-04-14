from django.conf.urls import url, include

from point.views import *
from point.public_views import *
from point.private_views import *

urlpatterns = [
    url(r'author_pointer_list/$', AuthorPointerList.as_view(), name="author_pointer_list"),
    url(r'join_pointer/(?P<pk>[0-9]+)/$', JoinPublicPointer.as_view(), name="join_pointer"),
    url(r'create_public_pointer/$', CreatePublicPointer.as_view(), name="create_public_pointer"),
    url(r'create_private_pointer/$', CreatePrivatePointer.as_view(), name="create_private_pointer"),
    url(r'delete_pointer/(?P<pk>[0-9]+)/$', DeletePointer.as_view(), name="delete_pointer"),
    url(r'user_story_list/$', UserPointerStory.as_view(), name="user_story_list"),
    url(r'storyline/$', StorylineViewSet.as_view(), name="storyline"),
    url(r'pointer_data/(?P<pk>[0-9]+)/$', PointerData.as_view(), name="pointer_data")
]
