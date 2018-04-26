from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from project.groups.models import Group
from project.modules.models import Module


class GroupAdminForm(forms.ModelForm):
    modules = forms.ModelMultipleChoiceField(
        queryset=Module.objects.all(),
        required=False,
        label="Задачи",
        widget=FilteredSelectMultiple(
            verbose_name="модули",
            is_stacked=False
        )
    )

    class Meta:
        model = Group
        fields = ['name', 'owners', 'members', "modules", "state", "codeword"]

    def save(self, commit=True):
        group = super(GroupAdminForm, self).save(commit=False)

        if group.state == 2 and group.codeword == "":
            raise forms.ValidationError("Обязательно кодовое слово")

        if commit:
            group.save()

        return group


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_root_owner', "state")
    fields = ['name', ('owners', 'members'), "modules", ("state", "codeword")]
    form = GroupAdminForm

admin.site.register(Group, GroupAdmin)
