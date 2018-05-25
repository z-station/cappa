from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.http import HttpResponseRedirect
from django.urls import reverse

from project.courses.models import TreeItem
from project.modules.models import Module


class ModuleAdminForm(forms.ModelForm):
    tasks = forms.ModelMultipleChoiceField(
        queryset=TreeItem.objects.all(),
        required=False,
        label="Задачи",
        widget=FilteredSelectMultiple(
            verbose_name="задачи",
            is_stacked=False
        )
    )

    class Meta:
        model = Module
        fields = ['name', 'comment', 'tasks']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'get_tasks_number', 'updated_at', 'id', )
    list_filter = ('updated_at', )
    search_fields = ('name', )
    fields = (('name', 'comment'), 'tasks', )
    form = ModuleAdminForm

    def response_add(self, request, obj, post_url_continue=None):
        if '_continue' not in request.POST:
            return HttpResponseRedirect(reverse('modules:my_modules'))
        else:
            return super(ModuleAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if '_continue' not in request.POST:
            return HttpResponseRedirect(reverse('modules:module', args=(obj.pk, )))
        else:
            return super(ModuleAdmin, self).response_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect(reverse('modules:my_modules'))

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super(ModuleAdmin, self).save_model(request, obj, form, change)
