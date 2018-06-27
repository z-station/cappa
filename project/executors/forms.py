from project.executors.models import Code, Executor, CodeTest
from django import forms
from project.executors.widgets import AceEditorAdminWidget


class ExecutorInlineForm(forms.ModelForm):
    class Meta:
        model = Executor
        fields = ("type_id",)

    type_id = forms.ChoiceField(
        label="Исполнитель", required=True,
        choices=Executor.EXEC_TYPES, initial=Executor.PYTHON36,
        help_text="так-же влияет на цветовую схему кода"
    )


class CodeForm(forms.ModelForm):
    """ Для user-интерфейса """
    class Meta:
        model = Code
        fields = ("input", "content", )

    class Media:
        js = (
            "js/ace/ace_init.js",
        )
    output = forms.CharField(
        label="Вывод", required=False,
        widget=forms.TextInput(attrs={"disabled": True})
    )
    error = forms.CharField(
        label="Ошибка", required=False,
        widget=forms.TextInput(attrs={"disabled": True})
    )


class CodeAdminForm(forms.ModelForm):
    """ Для Админ интерфейса """

    class Meta:
        model = Code
        fields = "__all__"
        widgets = {
            "content": AceEditorAdminWidget(),
            "input": AceEditorAdminWidget(),
            "solution": AceEditorAdminWidget(),
        }

    class Media:
        js = (
            "//code.jquery.com/jquery-3.3.1.min.js",
            "js/ace/ace_editor_v1.3.2.js",
            "js/ace/mode_python.js",
            "js/ace/ace_init.js",
        )
        css = {'all': ('css/ace/ace_admin.css',)}


class CodeInlineAdminForm(forms.ModelForm):
    """ Для Админ инлайн-интерфейса """

    class Meta:
        model = Code
        fields = "__all__"
        widgets = {
            "content": AceEditorAdminWidget(),
            "input": AceEditorAdminWidget(),
            "solution": AceEditorAdminWidget(),
        }

    class Media:
        js = (
            "js/ace/ace_editor_v1.3.2.js",
            "js/ace/mode_python.js",
            "js/ace/ace_init.js",
        )
        css = {'all': ('css/ace/ace_admin.css',)}

    def save(self, commit=True):
        if self.instance.treeitem and self.instance.treeitem.leaf:
            self.instance.show_input = True
            self.instance.show_tests = True
            self.instance.save_solutions = True
        return super(CodeInlineAdminForm, self).save(commit)


class CodeTestInlineAdminForm(forms.ModelForm):
    """ Для Админ инлайн-интерфейса """
    class Meta:
        model = CodeTest
        fields = ("input", "output", )
        widgets = {
            "input": AceEditorAdminWidget(),
            "output": AceEditorAdminWidget(),
        }
