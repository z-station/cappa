# -*- coding:utf-8 -*-
from django.conf.urls import url
from src.groups import views

urlpatterns = [
    url(r'^$', views.GroupListView.as_view(), name='groups'),
    url(r'^(?P<group_id>[0-9]+)/$', views.GroupView.as_view(), name='group'),
    url(r'^(?P<group_id>[0-9]+)/courses/(?P<group_course_id>[0-9]+)/$',
        views.GroupCourseView.as_view(),
        name='group-course'
    ),
    url(r'^(?P<group_id>[0-9]+)/courses/(?P<group_course_id>[0-9]+)/solutions/$',
        views.GroupCourseSolutionsView.as_view(),
        name='group-course-solutions'
    ),
]