from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponseRedirect
from django.contrib import admin

from app.databases.models import Database
from app.databases.service import DatabaseManagementService
from app.databases.enums import DatabaseStatus
from app.common.services import exceptions


@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):

    class Media:
        css = {'all': ('admin/databases/common.css',)}

    def get_status(self, obj):
        try:
            status = DatabaseManagementService.status(obj)
        except exceptions.ServiceException:
            return None
        else:
            return status == DatabaseStatus.ACTIVE
    get_status.boolean = True
    get_status.short_description = 'активная'
    raw_id_fields = ('author',)
    readonly_fields = ('get_status',)
    list_display = ('name', 'get_status', 'author')
    fields = (
        'get_status',
        'name',
        'author',
        'description',
        'file'
    )

    change_form_template = 'admin/databases/change_form.html'

    def response_change(self, request, obj):

        opts = self.model._meta
        preserved_filters = self.get_preserved_filters(request)
        if "create_db" in request.POST or "delete_db" in request.POST:
            try:
                if "create_db" in request.POST:
                    DatabaseManagementService.create(obj)
                    msg = 'Database created successfully!'
                elif "delete_db" in request.POST:
                    DatabaseManagementService.delete(obj)
                    msg = 'Database deleted successfully!'
                else:
                    msg = None
                msg_level = messages.SUCCESS
            except exceptions.ServiceException as ex:
                msg = f'{ex.message}\n{ex.details}'
                msg_level = messages.ERROR
            self.message_user(
                request=request,
                message=msg,
                level=msg_level
            )
            redirect_url = request.path
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)
        else:
            return super().response_change(request, obj)