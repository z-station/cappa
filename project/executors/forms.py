from project.executors.models import Code, Executor, EXECUTORS_NAMES, PYTHON36
from django import forms
from project.executors.widgets import AceEditorWidget


class ExecutorInlineForm(forms.ModelForm):
    class Meta:
        model = Executor
        fields = ("name",)
    name = forms.ChoiceField(label="Исполнитель", required=True,
                             choices=EXECUTORS_NAMES, initial=PYTHON36,
                             help_text="так-же влияет на цветовую схему кода")


class CodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ("content", "input", "output", )
        widgets = {
            "content": AceEditorWidget(),
            "input": AceEditorWidget(),
            "output": AceEditorWidget(),
        }


class CodeInlineForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = "__all__"
        widgets = {
            "content": AceEditorWidget(),
            "input": AceEditorWidget(),
            "output": AceEditorWidget(),
            "solution": AceEditorWidget(),
        }

    class Media:
        js = (
            "js/ace/ace_editor_v1.3.2.js",
            "js/ace/mode_python.js",
            "js/ace/ace_init.js",
        )
        css = {'all': ('css/ace/ace_admin.css',)}