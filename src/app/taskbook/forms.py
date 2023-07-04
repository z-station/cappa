from django import forms
from app.taskbook.models import TaskBookItem
from app.tasks.enums import TaskItemType
from app.translators.enums import TranslatorType


class TaskItemAdminForm(forms.ModelForm):

    class Meta:
        model = TaskBookItem
        fields = '__all__'

    translator = forms.TypedMultipleChoiceField(
        choices=TranslatorType.CHOICES
    )
    type = forms.CharField(
        initial=TaskItemType.TASKBOOK,
        widget=forms.HiddenInput()
    )
