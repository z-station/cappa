from django.contrib import admin
from django.forms import widgets
from adminsortable2.admin import SortableInlineAdminMixin
from src.quizzes.models import TaskItem, Solution
from src.quizzes.forms import TaskItemAdminForm
from src.utils.consts import langs


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
    fields = ('order_key', 'task', 'langg', 'max_score', 'compiler_check', 'manual_check', 'show')
#    fields = ('order_key', 'task', 'langs', 'max_score', 'compiler_check', 'manual_check', 'show')
    raw_id_fields = ("task",)


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):

    def get_user(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def status_name(self, obj):
        return obj.status_name
    status_name.short_description = 'статус'

    model = Solution
    # exclude = ('last_changes', 'version_list', 'version_best')
    # readonly_fields = ('status_name', 'tests_score', 'user', 'taskitem')
    list_display = ('get_user', 'taskitem', 'status_name')
    search_fields = ('user__first_name', 'user__last_name')
