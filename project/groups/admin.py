from django.contrib import admin

from project.groups.models import Group


class GroupAdmin(admin.ModelAdmin):
    model = Group
    list_display = ('id', 'name', 'display_root_owner')
    fields = ['name', ('owners', 'members'), 'modules']

admin.site.register(Group, GroupAdmin)
