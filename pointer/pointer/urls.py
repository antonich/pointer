from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.authtoken import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^users/', include('users.urls')),
    url(r'^friends/', include('friends.urls')),
    url(r'^point/', include('point.urls')),
]
