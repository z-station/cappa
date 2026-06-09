# -*- coding:utf-8 -*-
from django.urls import path
from app.groups import views

app_name = 'groups'

urlpatterns = [
    path('', views.GroupListView.as_view(), name='groups'),
    path('<int:group_id>/', views.GroupView.as_view(), name='group'),
    path(
        '<int:group_id>/statistics/',
        views.GroupCourseStatisticsView.as_view(),
        name='group-course-statistics'
    ),
    path(
        '<int:group_id>/plag-statistics/',
        views.GroupCoursePlagStatisticsView.as_view(),
        name='group-course-plag-statistics'
    ),
]
