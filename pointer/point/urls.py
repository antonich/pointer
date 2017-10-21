from django.conf.urls import url, include

from point.views import *

urlpatterns = [
    url(r'pointer_list/$', PointerList.as_view()),
]
