from django.contrib import admin
from project.sources.models import Source


class SourceAdmin(admin.ModelAdmin):
    model = Source


admin.site.register(Source, SourceAdmin)
