# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2024-05-25 22:00
from __future__ import unicode_literals

from django.db import migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0003_auto_20231113_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='file',
            field=filebrowser.fields.FileBrowseField(
                help_text='Файл данных PostgreSQL версии не ниже 13',
                max_length=1000,
                unique=True,
                verbose_name='файл'
            ),
        ),
    ]