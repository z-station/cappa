# -*- coding:utf-8 -*-
from django.contrib import admin
from project.executors.models import *
from project.executors.forms import *
from project.executors.nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedInline
from project.courses.admin import TreeItemAdmin, TreeItemFlatAdmin
from project.courses.models import TreeItem, TreeItemFlat


class ExecutorInlineAdmin(NestedStackedInline, admin.StackedInline):
    model = Executor
    form = ExecutorInlineForm
    extra = 0
    max_num = 1
    inlines = []


class UserSolutionAdmin(admin.ModelAdmin):

    def get_code_title(self, obj):
        return obj.code.get_title()
    get_code_title.short_description = "Элемент курса"

    def get_progress_percent(self, obj):
        return str(obj.progress) + '%'
    get_progress_percent.short_description = "Прогресс"

    model = UserSolution
    list_display = ("user", "code", "get_code_title", "get_progress_percent")
    search_fields = ["user__username", ]
    # readonly_fields = ("progress", "code", "user", "details",)

    def has_add_permission(self, request):
        """ Отключает возможность добавления решений через админку - только просмотр """
        return False

admin.site.register(UserSolution, UserSolutionAdmin)


class CodeTestInlineAdmin(admin.TabularInline):
    model = CodeTest
    form = CodeTestInlineAdminForm
    extra = 0
    inlines = []


class CodeFlatAdmin(admin.ModelAdmin):

    def get_author(self, obj):
        return obj.get_author()

    get_author.short_description = "Автор элемента курса"

    model = CodeFlat
    form = CodeAdminForm
    list_display = ("__str__", "description", "treeitem", "get_author")
    list_editable = ("treeitem", )
    inlines = [CodeTestInlineAdmin, ]
    search_fields = ("id", "treeitem__title", "treeitem__author")

admin.site.register(CodeFlat, CodeFlatAdmin)


class CodeTestNestedInlineAdmin(NestedInline):
    model = CodeTest
    form = CodeTestInlineAdminForm
    extra = 5
    classes = ("collapse", )
    inlines = []


class CodeInlineAdmin(NestedStackedInline, admin.StackedInline):
    model = Code
    extra = 0
    form = CodeInlineAdminForm
    inlines = [CodeTestNestedInlineAdmin, ]
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

# Добавить инлайн кода и исполнителя к моделям курсов
admin.site.unregister(TreeItem)
if not CodeInlineAdmin in TreeItemAdmin.inlines:
    TreeItemAdmin.inlines = list(TreeItemAdmin.inlines)[:] + [CodeInlineAdmin]
if not ExecutorInlineAdmin in TreeItemAdmin.inlines:
    TreeItemAdmin.inlines = list(TreeItemAdmin.inlines)[:] + [ExecutorInlineAdmin]
admin.site.register(TreeItem, TreeItemAdmin)

admin.site.unregister(TreeItemFlat)
if not CodeInlineAdmin in TreeItemFlatAdmin.inlines:
    TreeItemFlatAdmin.inlines = list(TreeItemFlatAdmin.inlines)[:] + [CodeInlineAdmin]
if not ExecutorInlineAdmin in TreeItemFlatAdmin.inlines:
    TreeItemFlatAdmin.inlines = list(TreeItemFlatAdmin.inlines)[:] + [ExecutorInlineAdmin]
admin.site.register(TreeItemFlat, TreeItemFlatAdmin)