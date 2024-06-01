# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2024-05-25 22:00
from __future__ import unicode_literals

import app.common.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20231113_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=app.common.fields.AnyExtFileBrowseField(blank=True, max_length=1000, null=True, verbose_name='изображение'),
        ),
    ]