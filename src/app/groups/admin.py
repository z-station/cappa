from django.contrib import admin
from app.groups.models import Group, GroupCourse, GroupMember
from app.groups.forms import GroupMemberAdminForm


class GroupMemberInline(admin.TabularInline):

    verbose_name = 'участник группы'
    verbose_name_plural = 'участники группы'
    model = GroupMember
    raw_id_fields = ['user']
    form = GroupMemberAdminForm
    extra = 0


class UserGroupInline(admin.TabularInline):

    verbose_name = 'учебная группа'
    verbose_name_plural = 'учебные группы'
    model = GroupMember
    raw_id_fields = ['group']
    form = GroupMemberAdminForm
    extra = 0


class GroupCourseInline(admin.TabularInline):
    model = GroupCourse
    extra = 0


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):

    def owner_full_name(self, obj):
        owner = obj.owner
        if owner:
            return f'{owner.last_name} {owner.first_name} {owner.father_name}'
        else:
            return '-'
    owner_full_name.short_description = 'Владелец группы'

    model = Group
    raw_id_fields = ('owner',)
    inlines = [GroupCourseInline, GroupMemberInline]
    list_display = ['title', 'year', 'owner_full_name', 'is_active']
    list_filter = ('year', 'is_active')
    search_fields = ('title',)
    exclude = ('members',)
