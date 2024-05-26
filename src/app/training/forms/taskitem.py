from django import forms
from app.tasks.models.taskitem import TaskItem
from app.tasks.enums import TaskItemType
from app.translators.enums import TranslatorType


class TaskItemAdminForm(forms.ModelForm):

    class Meta:
        model = TaskItem
        fields = '__all__'

    type = forms.CharField(
        initial=TaskItemType.COURSE,
        widget=forms.HiddenInput()
    )
    translator = forms.TypedMultipleChoiceField(
        choices=TranslatorType.CHOICES
    )
