from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Task, Source
from .forms import TaskAdminForm


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    class Media:
        css = {'all': ('admin/tasks/style.css',)}
        js = (
            'django_tinymce/jquery-1.9.1.min.js',
            'admin/tasks/jsoneditor.min.js',
            'admin/tasks/jsoneditor_init.js'
        )

    model = Task
    form = TaskAdminForm
    exclude = ('order_key',)
    raw_id_fields = ("author",)
    list_filter = ('source',)
    search_fields = ('title',)
    list_display = ('title', 'source', 'show')


@admin.register(Source)
class SourceAdmin(SortableAdminMixin, admin.ModelAdmin):

    model = Source
