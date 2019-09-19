# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from project.courses.models import TreeItem
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Command(BaseCommand):

    """ Обновить структуру решений (единовременная процедура)"""

    def handle(self, *args, **options):
        mig19 = UserModel.objects.get(id=6)

        for t in TreeItem.objects.all():
            t.author = mig19
            t.save()