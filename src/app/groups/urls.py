# -*- coding:utf-8 -*-
from django.conf.urls import url
from app.groups import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.GroupListView.as_view(),
        name='groups'
    ),
    url(
        regex=r'^(?P<group_id>[0-9]+)/$',
        view=views.GroupView.as_view(),
        name='group'
        ),
    url(
        regex=r'^(?P<group_id>[0-9]+)/statistics/$',
        view=views.GroupCourseStatisticsView.as_view(),
        name='group-course-statistics'
    ),
    url(
        regex=r'^(?P<group_id>[0-9]+)/plag-statistics/$',
        view=views.GroupCoursePlagStatisticsView.as_view(),
        name='group-course-plag-statistics'
    )
]
