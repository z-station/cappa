from django.conf.urls import url

from . import views

app_name = 'groups'
urlpatterns = [
    url(r'^$', views.GroupsView.as_view(), name='groups'),
    url(r'^(?P<pk>[0-9]+)/$', views.GroupView.as_view(), name='group'),
    url(r'^(?P<pk>[0-9]+)/join/$', views.join, name='join'),
]
