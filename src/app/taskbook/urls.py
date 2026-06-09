# -*- coding:utf-8 -*-
from django.urls import path
from app.taskbook import views

app_name = 'taskbook'

urlpatterns = [
    path('', views.TaskBookView.as_view(), name='taskbook'),
    path('<slug:taskitem>/', views.TaskItemView.as_view(), name='taskitem'),
]
