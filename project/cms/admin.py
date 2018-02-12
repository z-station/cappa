# -*- coding:utf-8 -*-
from catalog.admin import CatalogItemBaseAdmin
from .models import Course, Task, Topic
from django.contrib import admin


class CourseAdmin(CatalogItemBaseAdmin):
    model = Course


admin.site.register(Course, CourseAdmin)


class TopicAdmin(CatalogItemBaseAdmin):
    model = Topic


admin.site.register(Topic, TopicAdmin)


class TaskAdmin(CatalogItemBaseAdmin):
    model = Task


admin.site.register(Task, TaskAdmin)

