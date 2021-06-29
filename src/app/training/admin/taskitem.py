from django.contrib import admin
from django.forms import widgets
from adminsortable2.admin import SortableInlineAdminMixin
from app.training.models import TaskItem, Solution
from app.training.forms import TaskItemAdminForm


class TaskItemInline(SortableInlineAdminMixin, admin.TabularInline):

    @property
    def media(self):
        return (
            super(SortableInlineAdminMixin, self).media + widgets.Media(js=(
                'adminsortable2/js/libs/jquery.ui.sortable-1.11.4.js',
                'admin/training/inline-sortable.js',
                'adminsortable2/js/inline-tabular.js')
            )
        )

    model = TaskItem
    form = TaskItemAdminForm
    extra = 0
    fields = ('order_key', 'task', 'max_score', 'compiler_check', 'manual_check', 'one_try', 'show')
    raw_id_fields = ("task",)


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):

    def get_user(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def status_name(self, obj):
        return obj.status_name
    status_name.short_description = 'статус'

    model = Solution
    list_display = (
        'get_user',
        'taskitem',
        'status_name',
        'last_modified',
        'datetime',
    )
    search_fields = ('user__first_name', 'user__last_name', 'taskitem__task__title')
    exclude = ('last_changes',)
