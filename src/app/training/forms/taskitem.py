from django import forms


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
