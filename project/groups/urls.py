from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'groups'
urlpatterns = [
    url(r'^$', views.GroupsView.as_view(), name='groups'),
    url(r'^my_groups/$', login_required(views.MyGroupsView.as_view()), name='my_groups'),
    url(r'^(?P<pk>[0-9]+)/$', views.GroupView.as_view(), name='group'),
    url(r'^(?P<pk>[0-9]+)/join/$', login_required(views.join), name='join'),
]
