from django import forms
from app.groups.models import Group, GroupMember
from app.groups.enums import GroupMemberRole


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
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Кодовое слово',
                'class': 'form-control'
            }
        ), required=False
    )

    def clean(self):
        data = self.cleaned_data
        group = self.instance
        if group.user_is_learner or group.user_is_teacher:
            self.add_error(field=None, error='Вы уже являетесь участником группы')
        if self.instance.is_closed:
            self.add_error(field=None, error='Группа закрыта')
        elif self.instance.by_codeword:
            if data.get('code') != self.instance.codeword:
                self.add_error(field='code', error='Неверное кодовое слово')
        return data


class GroupMemberAdminForm(forms.ModelForm):

    class Meta:
        model = GroupMember
        fields = '__all__'

    def clean(self):
        user = self.cleaned_data.get('user')
        role = self.cleaned_data['role']
        if user and role == GroupMemberRole.TEACHER and not user.is_teacher:
            self.add_error(
                field='role',
                error='Пользователь не являетя преподавателем'
            )
        return self.cleaned_data
