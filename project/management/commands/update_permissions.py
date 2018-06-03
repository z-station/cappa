# -*- coding: utf-8 -*-
import sys
from django.core.management.base import BaseCommand
from django.contrib.auth.management import _get_all_permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class Command(BaseCommand):
    """ При создании пустой бд, для прокси моделей (по умолчанию) не создаются права
        команда создает права для моделей без прав(в частности прокси-моделей)"""

    def handle(self, *args, **options):
        help = "Fix permissions for proxy models."
        for model in apps.get_models():
            opts = model._meta
            ctype, created = ContentType.objects.get_or_create(
                app_label=opts.app_label,
                model=opts.object_name.lower(),
            )

            for codename, name in _get_all_permissions(opts):
                p, created = Permission.objects.get_or_create(
                    codename=codename,
                    content_type=ctype,
                )
                if created:
                    sys.stdout.write('Adding permission {}\n'.format(p))
