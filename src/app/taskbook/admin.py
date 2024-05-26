from django.contrib import admin
from app.taskbook.models import TaskBookItem
from app.taskbook.forms import TaskItemAdminForm


@admin.register(TaskBookItem)
class TaskItemAdmin(admin.ModelAdmin):

    model = TaskBookItem
    form = TaskItemAdminForm
    raw_id_fields = ('task',)
    readonly_fields = ('slug',)
    list_display = (
        'title',
        'show',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'show',
    )
    fields = (
        'show',
        'task',
        'max_score',
        'score_method',
        'translator',
        'database',
        'slug',
        'type',
    )

    def get_queryset(self, request):
        qst = super().get_queryset(request)
        return qst.type_taskbook()
