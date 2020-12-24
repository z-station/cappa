from django import forms
from .models import Group


class GroupSearchForm(forms.Form):

    search = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по названию группы',
            'class': 'form-control'
        }), required=False
    )


class GroupInviteForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = []

    error_css_class = 'error'

    code = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Кодовое слово',
            'class': 'form-control'
        }), required=False
    )

    def clean(self):
        data = self.cleaned_data
        if self.instance.status == Group.CLOSE:
            self.add_error(field=None, error='Группа закрыта')
        elif self.instance.status == Group.CODE:
            if data['code'] != self.instance.codeword:
                self.add_error(field='code', error='Неверное кодовое слово')
        elif self.instance.status == Group.OPEN:
            pass
        return data

