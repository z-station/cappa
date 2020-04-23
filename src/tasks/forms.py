from django import forms
from .models import Task, SolutionExample
from django.contrib.postgres.forms import JSONField
from src.widgets.ace import AceWidget
from src.widgets.json import JsonWidget


class TaskAdminForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'

    tests = JSONField(label='Тесты', widget=JsonWidget, required=False)


class SolutionExampleAdminForm(forms.ModelForm):

    class Meta:
        model = SolutionExample
        fields = '__all__'
        widgets = {'content': AceWidget}
