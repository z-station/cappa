from django.utils.encoding import force_text
from app.common.admin.actions import delete_selected


class DeleteSelectedMixin:

    def get_actions(self, request):

        """ Customize delete action """

        actions = super().get_actions(request)
        actions['delete_selected'] = (
            delete_selected,
            'delete_selected',
            delete_selected.short_description
        )
        return actions

    @staticmethod
    def perform_delete_selected(modeladmin, request, queryset):

        """ Perform delete many records """

        for obj in queryset:
            obj_display = force_text(obj)
            modeladmin.log_deletion(request, obj, obj_display)
        queryset.delete()
