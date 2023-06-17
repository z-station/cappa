from django.contrib import admin
from app.taskbook.models import TaskBookItem
from app.taskbook.forms import TaskBookItemAdminForm


@admin.register(TaskBookItem)
class TaskBookItemAdmin(admin.ModelAdmin):

    model = TaskBookItem
    form = TaskBookItemAdminForm
    raw_id_fields = ("task",)
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
