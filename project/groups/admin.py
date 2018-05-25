from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.functional import curry

from project.groups.models import Group, ModuleData
from project.modules.models import Module


class ModuleDataFormset(forms.models.BaseInlineFormSet):

    class Meta:
        model = ModuleData
        fields = ['module', 'state', 'open_at', 'close_at']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ModuleDataFormset, self).__init__(*args, **kwargs)

        if user:
            queryset = Module.objects.filter(owner__id=user.id)
            for form in self.forms:
                form.fields['module'].queryset = queryset


class ModuleDataInline(admin.TabularInline):
    model = ModuleData
    fields = ['module', 'state', 'open_at', 'close_at']
    verbose_name = 'Модуль в группе'
    verbose_name_plural = 'Модули в группе'
    formset = ModuleDataFormset
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(ModuleDataInline, self).get_formset(request, obj, **kwargs)
        if request.method == "GET":
            if getattr(obj, 'owners', None) is None:
                formset.__init__ = curry(formset.__init__, user=request.user)
            else:
                try:
                    formset.__init__ = curry(formset.__init__, user=obj.owners.all()[0])
                except IndexError:
                    pass
        return formset


class GroupAdminForm(forms.ModelForm):
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

    class Meta:
        model = Group
        fields = ['name', 'status', 'owners', 'members', 'state', 'codeword']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            kwargs.update(initial={
                'owners': user
            })

        super(GroupAdminForm, self).__init__(*args, **kwargs)

    def clean_codeword(self):
        codeword = self.cleaned_data['codeword']
        state = int(self.data.get('state'))
        if state == Group.CODE and codeword == '':
            raise forms.ValidationError('В этом случае, кодовое слово - обязательно')

        return codeword


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_root_owner_username', 'state', 'get_members_number', 'created_at', 'id', )
    list_filter = ('state', 'created_at', )
    search_fields = ('name', )
    fields = (('name', 'status'), ('owners', 'members'), ('state', 'codeword'), )
    inlines = (ModuleDataInline, )
    form = GroupAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(GroupAdmin, self).get_form(request, obj, **kwargs)
        if getattr(obj, 'owners', None) is None:
            return curry(form, user=request.user)
        # #owners
        # return form
        return curry(form, user=obj.owners.all()[0])

    def response_add(self, request, obj, post_url_continue=None):
        if '_continue' not in request.POST:
            return HttpResponseRedirect(reverse('groups:my_groups'))
        else:
            return super(GroupAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if '_continue' not in request.POST:
            return HttpResponseRedirect(reverse('groups:group', args=(obj.pk, )))
        else:
            return super(GroupAdmin, self).response_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect(reverse('groups:my_groups'))

    def save_model(self, request, obj, form, change):
        # #owners
        # form.cleaned_data['owners'] |= User.objects.filter(pk=form.cleaned_data['owners'].pk)
        # form.cleaned_data['members'] = form.cleaned_data['members']\
        #     .exclude(pk__in=[owner.pk for owner in form.cleaned_data['owners'].all()])
        form.cleaned_data['members'] = form.cleaned_data['members'].exclude(pk=form.cleaned_data['owners'].pk)
        form.cleaned_data['owners'] = User.objects.filter(pk=form.cleaned_data['owners'].pk)

        super(GroupAdmin, self).save_model(request, obj, form, change)
