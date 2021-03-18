# -*- coding utf-8 -*-
from django.contrib import admin
from django.contrib.sites.admin import Site
from app.service.models import SiteSettings


admin.site.unregister(Site)
admin.site.register(SiteSettings)
