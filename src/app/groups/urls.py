# -*- coding:utf-8 -*-
from django.conf.urls import url
from app.groups import views

urlpatterns = [
    url(r'^$', views.GroupListView.as_view(), name='groups'),
    url(r'^(?P<group_id>[0-9]+)/$', views.GroupView.as_view(), name='group'),
    url(
        r'^(?P<group_id>[0-9]+)/statistics/$',
        views.GroupCourseStatisticsView.as_view(),
        name='group-course-statistics'
    ),
    url(
        r'^(?P<group_id>[0-9]+)/plag-statistics/$',
        views.GroupCoursePlagStatisticsView.as_view(),
        name='group-course-plag-statistics'
    )
]
