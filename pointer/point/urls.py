from django.conf.urls import url, include

from point.views import *
from point.public_views import *

urlpatterns = [
    url(r'author_pointer_list/', AuthorPointerList.as_view(), name="author_pointer_list"),
    url(r'join_pointer/(?P<pk>[0-9]+)/$', JoinPublicPointer.as_view(), name="join_pointer"),
    url(r'create_public_pointer/$', CreatePublicPointer.as_view(), name="create_public_pointer"),
]
