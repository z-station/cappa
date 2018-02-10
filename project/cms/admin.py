# -*- coding:utf-8 -*-
from catalog.admin import CatalogItemBaseAdmin
from .models import Course, Task, Topic
from django.contrib import admin


class CourseAdmin(CatalogItemBaseAdmin):
    model = Course


admin.register(Course, CourseAdmin)


class TopicAdmin(CatalogItemBaseAdmin):
    model = Topic


admin.register(Topic, TopicAdmin)


class TaskAdmin(CatalogItemBaseAdmin):
    model = Task


admin.register(Task, TaskAdmin)

