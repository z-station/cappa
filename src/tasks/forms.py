from django import forms
from .models import Task
from .widgets import JsonWidget
from django.contrib.postgres.forms import JSONField


class TaskAdminForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'

    tests = JSONField(label='Тесты', widget=JsonWidget, required=False)
