from django.contrib import admin
from src.groups.models import Group, GroupCourse, GroupMember, GroupQuiz


class GroupMemberInline(admin.TabularInline):

    model = GroupMember
    raw_id_fields = ['user']
    extra = 0


class GroupCourseInline(admin.TabularInline):
    model = GroupCourse
    extra = 0
    

class GroupQuizInline(admin.TabularInline):
    model = GroupQuiz
    extra = 0

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):

    model = Group
    raw_id_fields = ['author']
    inlines = [GroupCourseInline, GroupQuizInline, GroupMemberInline]
    list_display = ['title', 'author', 'show']
    exclude = ('_members',)