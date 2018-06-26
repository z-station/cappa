# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from project.groups.models import Group, GroupModule
from project.modules.models import Module


class GroupModuleFormset(forms.models.BaseInlineFormSet):

    class Meta:
        model = GroupModule
        fields = ['module', 'state', 'open_at', 'close_at']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GroupModuleFormset, self).__init__(*args, **kwargs)

        if user:
            queryset = Module.objects.filter(owner__id=user.id)
            for form in self.forms:
                form.fields['module'].queryset = queryset


class GroupAdminForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name', 'status', 'owners', 'members', 'state', 'codeword']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            kwargs.update(initial={
                'owners': user,
            })

        super(GroupAdminForm, self).__init__(*args, **kwargs)

    # #owners
    # owners = forms.ModelMultipleChoiceField(
    #     queryset=User.objects.all(),
    #     required=False,
    #     label='Владельцы',
    #     widget=FilteredSelectMultiple(
    #         verbose_name='пользователи',
    #         is_stacked=False
    #     )
    # )
    owners = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Владелец',
    )
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Участники',
        widget=FilteredSelectMultiple(
            verbose_name='пользователи',
            is_stacked=False
        )
    )

    def clean_codeword(self):
        codeword = self.cleaned_data['codeword']
        state = int(self.data.get('state'))
        if state == Group.CODE and codeword == '':
            raise forms.ValidationError('В этом случае, кодовое слово - обязательно')
        return codeword
