from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.functional import curry

from project.groups.forms import GroupModuleFormset, GroupAdminForm
from project.groups.models import Group, GroupModule
from project.utils import check_custom_response


class GroupModuleInline(admin.TabularInline):
    model = GroupModule
    fields = ['module', 'state', 'open_at', 'close_at']
    verbose_name = 'Модуль в группе'
    verbose_name_plural = 'Модули в группе'
    formset = GroupModuleFormset
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(GroupModuleInline, self).get_formset(request, obj, **kwargs)
        if request.method == "GET":
            if getattr(obj, 'owners', None) is None:
                formset.__init__ = curry(formset.__init__, user=request.user)
            else:
                try:
                    formset.__init__ = curry(formset.__init__, user=obj.owners.all()[0])
                except IndexError:
                    pass
        return formset


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_root_username', 'state', 'get_members_number', 'created_at', 'id', )
    list_filter = ('state', 'created_at', )
    search_fields = ('name', )
    fields = (('name', 'status'), ('owners', 'members'), ('state', 'codeword'), )
    inlines = (GroupModuleInline, )
    form = GroupAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(GroupAdmin, self).get_form(request, obj, **kwargs)
        if getattr(obj, 'owners', None) is None:
            return curry(form, user=request.user)
        # #owners
        # return form
        try:
            return curry(form, user=obj.owners.all()[0])
        except IndexError:
            return curry(form, user=None)

    # def response_add(self, request, obj, post_url_continue=None):
    #     if check_custom_response(request):
    #         messages.success(request, 'Группа "{}" была успешно добавлена!'.format(obj.name))
    #         return HttpResponseRedirect(reverse('groups:group', args=(obj.pk,)))
    #     else:
    #         return super(GroupAdmin, self).response_add(request, obj, post_url_continue)
    #
    # def response_change(self, request, obj):
    #     if check_custom_response(request):
    #         messages.success(request, 'Группа "{}" была успешно изменена!'.format(obj.name))
    #         return HttpResponseRedirect(reverse('groups:group', args=(obj.pk,)))
    #     else:
    #         return super(GroupAdmin, self).response_change(request, obj)
    #
    # def response_delete(self, request, obj_display, obj_id):
    #     messages.success(request, 'Группа "{}" была успешно удалена!'.format(obj_display))
    #     return HttpResponseRedirect(reverse('groups:my_groups'))

    def save_model(self, request, obj, form, change):
        # #owners
        # form.cleaned_data['owners'] |= User.objects.filter(pk=form.cleaned_data['owners'].pk)
        # form.cleaned_data['members'] = form.cleaned_data['members']\
        #     .exclude(pk__in=[owner.pk for owner in form.cleaned_data['owners'].all()])
        form.cleaned_data['members'] = form.cleaned_data['members'].exclude(pk=form.cleaned_data['owners'].pk)
        form.cleaned_data['owners'] = User.objects.filter(pk=form.cleaned_data['owners'].pk)

        super(GroupAdmin, self).save_model(request, obj, form, change)
