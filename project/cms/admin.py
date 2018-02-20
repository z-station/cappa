# -*- coding:utf-8 -*-
from catalog.admin import CatalogItemBaseAdmin
from .models import Course, Task, Topic
from django.contrib import admin


class CourseAdmin(CatalogItemBaseAdmin):
    model = Course
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('executors', )


admin.site.register(Course, CourseAdmin)


class TopicAdmin(CatalogItemBaseAdmin):
    model = Topic
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Topic, TopicAdmin)


class TaskAdmin(CatalogItemBaseAdmin):
    model = Task
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Task, TaskAdmin)

