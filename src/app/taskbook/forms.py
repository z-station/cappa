from django import forms
from app.tasks.models import TaskItem
from app.tasks.enums import TaskItemType
from app.translators.enums import TranslatorType


class TaskItemAdminForm(forms.ModelForm):

    class Meta:
        model = TaskItem
        fields = '__all__'

    translator = forms.TypedMultipleChoiceField(
        choices=TranslatorType.CHOICES
    )
    type = forms.CharField(
        initial=TaskItemType.TASKBOOK,
        widget=forms.HiddenInput()
    )
