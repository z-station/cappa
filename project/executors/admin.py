# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from project.executors.models import Executor, Code
from project.executors.forms import CodeInlineForm, ExecutorInlineForm
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class ExecutorAdmin(admin.ModelAdmin):
    model = Executor

admin.site.register(Executor, ExecutorAdmin)


class ExecutorInline(GenericTabularInline):
    model = Executor
    form = ExecutorInlineForm
    extra = 0
    max_num = 1


class CodeInline(GenericStackedInline):
    model = Code
    form = CodeInlineForm
    extra = 0
    fieldsets = (
        (
            "Код", {
                "fields": ("content",("type", "executor",),),
                "classes": ("collapse",),
            }
        ),
        (
            "Решение", {
                "fields": ("solution",),
                "classes": ("collapse",),
            }
        ),
        (
            "Ввод/вывод", {
                "fields": ("input", "output",),
                "classes": ("collapse",),
            }
        ),
    )

if not hasattr(settings, 'CODE_FOR_MODELS'):
    raise ImproperlyConfigured('Please add "CODE_FOR_MODELS = ["<project>.<app>.models.<Model>",]" to your settings.py')

for model_path in settings.CODE_FOR_MODELS:
    model_dir, model_name = model_path.rsplit(".", 1)
    model = __import__(model_dir, globals(), locals(), [model_name, ])
    model = getattr(model, model_name)
    model_admin = admin.site._registry[model].__class__
    admin.site.unregister(model)

    setattr(model_admin, 'inlines', getattr(model_admin, 'inlines', []))
    if not CodeInline in model_admin.inlines:
        model_admin.inlines = list(model_admin.inlines)[:] + [CodeInline]
    if not ExecutorInline in model_admin.inlines:
        model_admin.inlines = list(model_admin.inlines)[:] + [ExecutorInline]

    admin.site.register(model, model_admin)
