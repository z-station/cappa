# -*- coding: utf-8 -*-
from app.service.models import SiteSettings
from django.conf import settings


def site_settings(request):
    return {
        "site": SiteSettings.objects.filter(id=settings.SITE_ID).first()
    }
