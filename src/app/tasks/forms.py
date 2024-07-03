from django import forms
from app.tasks.models import (
    Task,
    Solution,
    SolutionExample,
    ExternalSolution,
    Checker,
)
from app.tasks.enums import ReviewStatus
from django.contrib.postgres.forms import JSONField
from app.common.widgets import (
    AceWidget,
    JsonWidget
)
from tinymce.widgets import TinyMCE


class TaskAdminForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'

    tests = JSONField(label='Тесты', widget=JsonWidget, required=False)


class ExternalSolutionAdminForm(forms.ModelForm):

    class Meta:
        model = ExternalSolution
        fields = "__all__"
        widgets = {
            'content': AceWidget,
        }


class SolutionAdminForm(forms.ModelForm):

    class Meta:
        model = Solution
        fields = "__all__"
        widgets = {
            'content': AceWidget,
        }


class SolutionExampleAdminForm(forms.ModelForm):

    class Meta:
        model = SolutionExample
        fields = '__all__'
        widgets = {'content': AceWidget}


class CheckerAdminForm(forms.ModelForm):

    class Meta:
        model = Checker
        fields = '__all__'
        widgets = {
            'content': AceWidget,
        }



class ReviewSolutionForm(forms.ModelForm):

    class Meta:
        model = Solution
        fields = (
            'review_status',
            'review_score',
            'reviewer_comment',
            'hide_review_score',
            'hide_reviewer_comment',
        )

    review_status = forms.CharField(
        label='Статус проверки',
        widget=forms.Select(
            attrs={'class': 'form-control'},
            choices=ReviewStatus.CHOICES
        )
    )
    review_score = forms.FloatField(
        label='Оценка',
        required=False,
        widget=forms.NumberInput(
            attrs={'step': '0.01', 'class': 'form-control'}
        )
    )
    reviewer_comment = forms.CharField(
        label='Комментарий преподавателя',
        widget=TinyMCE,
        required=False
    )
    hide_review_score = forms.BooleanField(
        label="скрыть оценку",
        required=False,
        widget=forms.CheckboxInput()
    )
    hide_reviewer_comment = forms.BooleanField(
        label="скрыть комментарий",
        required=False,
        widget=forms.CheckboxInput()
    )


class EditorForm(forms.Form):

    input = forms.CharField(
        label="Консольный ввод",
        required=False
    )
    content = forms.CharField(label='Код программы')
    output = forms.CharField(
        label="Консольный вывод",
        required=False,
        widget=forms.Textarea(attrs={'readonly': True})
    )
    error = forms.CharField(
        label="Ошибка отладки",
        required=False,
        widget=forms.Textarea(attrs={'readonly': True})
    )
    translator = forms.CharField(widget=forms.HiddenInput)
    db_name = forms.CharField(widget=forms.HiddenInput)


class SqlEditorForm(forms.Form):

    content = forms.CharField(label='Код запроса')
    output = forms.CharField(
        label="Результат запроса",
        required=False,
        widget=forms.Textarea(attrs={'readonly': True})
    )
    error = forms.CharField(
        label="Ошибка",
        required=False,
        widget=forms.Textarea(attrs={'readonly': True})
    )
    translator = forms.CharField(widget=forms.HiddenInput)
    db_name = forms.CharField(widget=forms.HiddenInput)
