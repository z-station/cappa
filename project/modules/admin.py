from django.contrib import admin

from project.modules.models import Module


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')
    exclude = ('courses', 'units')

admin.site.register(Module, ModuleAdmin)
