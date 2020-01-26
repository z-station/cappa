from django.contrib import admin
from django.forms import widgets
from adminsortable2.admin import SortableInlineAdminMixin
from src.training.models import TaskItem, Solution


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
    extra = 0
    fields = ('order_key', 'task', 'show')
    raw_id_fields = ("task",)


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):

    def get_user(self, obj):
        return obj.user.get_full_name() or obj.user.username

    model = Solution
    exclude = ('last_changes', 'version_list')
    readonly_fields = ('progress', 'status')
    raw_id_fields = ('user', 'taskitem')
    list_display = ('get_user', 'taskitem', 'progress')
    search_fields = ('user__first_name', 'user__last_name')