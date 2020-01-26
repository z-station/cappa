from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Task, Source


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    model = Task
    exclude = ('order_key',)
    raw_id_fields = ("author",)
    list_filter = ('source',)
    search_fields = ('title',)
    list_display = ('title', 'source', 'show')

@admin.register(Source)
class SourceAdmin(SortableAdminMixin, admin.ModelAdmin):

    model = Source
