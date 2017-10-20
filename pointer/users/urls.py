from django.conf.urls import url, include

from users import views

urlpatterns = [
    url(r'register/$', views.UserCreationView.as_view()),
    url(r'login/$', views.UserLoginView.as_view()),
    url(r'^activate/(?P<key>\w{8,16})/?$', views.UserActivationView.as_view()),
    url(r'^logout/$', views.UserLogoutView.as_view())
]
