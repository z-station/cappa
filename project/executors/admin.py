# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from project.executors.models import Executor, Code, CodeTest, CodeSolution
from project.executors.forms import *
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from project.executors.nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedInline


class ExecutorInlineAdmin(NestedStackedInline, GenericStackedInline):
    model = Executor
    form = ExecutorInlineForm
    extra = 0
    max_num = 1
    inlines = []


admin.site.register(CodeSolution)


class CodeTestInlineAdmin(NestedInline):
    model = CodeTest
    form = CodeTestInlineAdminForm
    extra = 0
    classes = ("collapse", )
    inlines = []


class CodeInlineAdmin(NestedStackedInline, GenericStackedInline):
    model = Code
    extra = 0
    form = CodeInlineAdminForm
    inlines = [CodeTestInlineAdmin, ]
    fieldsets = (
        (
            "Код", {
                "fields": ("input", "content",),
                "classes": ("collapse",),
            }
        ),
        (
            "Эталонное решение", {
                "fields": ("solution",),
                "classes": ("collapse",),
            }
        ),
        (
            "Настройки", {
                "fields": ("type", "executor_type_id", "show_input", "show_tests",  "save_solutions",
                           "input_max_signs", "content_max_signs", "timeout"),
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
    if not CodeInlineAdmin in model_admin.inlines:
        model_admin.inlines = list(model_admin.inlines)[:] + [CodeInlineAdmin]
    if not ExecutorInlineAdmin in model_admin.inlines:
        model_admin.inlines = list(model_admin.inlines)[:] + [ExecutorInlineAdmin]

    admin.site.register(model, model_admin)
