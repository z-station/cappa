# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


def create_tokens(*args, **kwargs):
    UserModel = get_user_model()
    for user in UserModel.objects.all():
        Token.objects.get_or_create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0013_drop_lang_id'),
    ]

    operations = [
        migrations.RunPython(
            code=create_tokens
        )
    ]
