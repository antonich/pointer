from django.conf.urls import url, include

from members import views

urlpatterns = [
    url(r'members_list/(?P<pk>[0-9]+)/$', views.MemberListView.as_view(), name="members_list"),
    url(r'going_members/(?P<pk>[0-9]+)/$', views.GoingMemberListView.as_view(), name="going_members_list"),
    url(r'decline_members/(?P<pk>[0-9]+)/$', views.DeclineMemberListView.as_view(), name="decline_members_list"),
]
