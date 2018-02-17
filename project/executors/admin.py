# -*- coding:utf-8 -*-
from django.contrib import admin
from project.executors.models import Executor


class ExecutorAdmin(admin.ModelAdmin):
    model = Executor

admin.site.register(Executor, ExecutorAdmin)
