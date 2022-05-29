from django.contrib import admin
from django.forms import widgets
from adminsortable2.admin import SortableInlineAdminMixin
from app.training.models import TaskItem


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
    fields = ('order_key', 'task', 'max_score', 'score_method', 'show')
    raw_id_fields = ("task",)
