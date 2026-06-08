# -*- coding utf-8 -*-
from django.contrib import admin
from django.contrib.sites.admin import Site

from app.service.models import SiteSettings
from app.auth.utils import logout_users_by_access_type


class SiteSettingsAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        old_signin = None
        if change and obj.pk:
            old_signin = SiteSettings.objects.get(pk=obj.pk).signin
        super().save_model(request, obj, form, change)
        if (
            change
            and old_signin is not None
            and old_signin != obj.signin
        ):
            logout_users_by_access_type(obj.signin)


admin.site.unregister(Site)
admin.site.register(SiteSettings, SiteSettingsAdmin)
