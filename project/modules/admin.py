from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from project.cms.models import Task
from project.modules.models import Module


class ModuleAdminForm(forms.ModelForm):
    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        required=False,
        label="Задачи",
        widget=FilteredSelectMultiple(
            verbose_name="задачи",
            is_stacked=False
        )
    )

    class Meta:
        model = Module
        fields = ['name', 'owner', 'tasks']


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')
    form = ModuleAdminForm

admin.site.register(Module, ModuleAdmin)
