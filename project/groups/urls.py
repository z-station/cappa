# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from project.groups import views
from project.modules.views import ModuleProgressView

app_name = 'groups'
urlpatterns = [
    url(r'^$', views.GroupsView.as_view(), name='groups'),
    url(r'^my_groups/$', login_required(views.MyGroupsView.as_view()), name='my_groups'),
    url(r'^(?P<pk>[0-9]+)/$', views.GroupView.as_view(), name='group'),
    url(r'^(?P<pk>[0-9]+)/progress/$', views.GroupProgressView.as_view(), name='progress'),
    url(r'^(?P<group_id>[0-9]+)/modules/(?P<pk>[0-9]+)/$', ModuleProgressView.as_view(), name='module_progress'),
    url(r'^(?P<group_id>[0-9]+)/courses/(?P<course_id>[0-9]+)/$', views.GroupCourse.as_view(), name='group_course'),
    url(r'^(?P<group_id>[0-9]+)/courses/(?P<course_id>[0-9]+)/themes/(?P<theme_id>[0-9]+)/$', views.group_course_theme, name='group_course_theme'),
    url(r'^(?P<group_id>[0-9]+)/join/$', login_required(views.join), name='join'),
]

"""
    доступ через профиль
    группы/  - список групп
    группа/1/ - список участников, какая -то инфа по группе + список модулей
    группа/1/модуль/1/ - страница модуля - общая инфа + личные результаты по модулю + список заданий

    для учителя:
    группа/1/модуль/1/итоги/ - итоги по конкретному модулю в группе
    группа/1/итоги/  -  итоги по группе по всем модулям(продумать)

"""
