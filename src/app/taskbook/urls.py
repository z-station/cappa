# -*- coding:utf-8 -*-
from django.conf.urls import url
from app.taskbook import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.TaskBookView.as_view(),
        name='taskbook'
    ),
    url(
        regex=r'^taskitem/',
        view=views.TaskBookTaskitemView.as_view(),
        name='taskitem'
    )
]
