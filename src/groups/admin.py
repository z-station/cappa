from django.contrib import admin
from src.groups.models import Group, GroupCourse, GroupMember


class GroupMemberInline(admin.TabularInline):

    model = GroupMember
    raw_id_fields = ['user']
    extra = 0


class GroupCourseInline(admin.TabularInline):
    model = GroupCourse
    extra = 0


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):

    model = Group
    raw_id_fields = ['author']
    inlines = [GroupCourseInline, GroupMemberInline]
    list_display = ['title', 'author', 'show']
    exclude = ('_members',)