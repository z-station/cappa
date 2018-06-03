# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from project.groups.views import GroupsView, MyGroupsView, GroupView, progress, join

app_name = 'groups'
urlpatterns = [
    url(r'^$', GroupsView.as_view(), name='groups'),
    url(r'^my_groups/$', MyGroupsView.as_view(), name='my_groups'),
    url(r'^(?P<pk>[0-9]+)/$', GroupView.as_view(), name='group'),
    url(r'^(?P<group_id>[0-9]+)/progress/$', progress, name='progress'),
    url(r'^(?P<pk>[0-9]+)/join/$', join, name='join'),
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