from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter, ChoiceDropdownFilter
from .models import Task, Tag, SolutionExample, Source
from .forms import TaskAdminForm, SolutionExampleAdminForm


class SolutionExampleInline(admin.StackedInline):

    model = SolutionExample
    form = SolutionExampleAdminForm
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    class Media:
        css = {'all': ('admin/tasks/style.css',)}
        js = (
            'django_tinymce/jquery-1.9.1.min.js',
            'admin/tasks/jsoneditor.min.js',
            'js/ace-1.4.7/ace.js',
            'admin/tasks/task.js'
        )

    model = Task
    form = TaskAdminForm
    exclude = ('order_key',)
    raw_id_fields = ("author",)
    search_fields = ('title',)
    list_display = ('title',)
    filter_horizontal = ('tags',)
    inlines = (SolutionExampleInline,)
    list_filter = (
        ('lang', ChoiceDropdownFilter),
        ('tags', RelatedDropdownFilter),
        ('difficulty', ChoiceDropdownFilter),
        ('source', RelatedDropdownFilter),
    )


admin.site.register(Tag)
admin.site.register(Source)
