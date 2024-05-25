# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-11-13 17:12
from __future__ import unicode_literals

import app.databases.utils
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0002_auto_20220615_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='file',
            field=models.FileField(
                help_text='Файл данных PostgreSQL версии не ниже 13',
                storage=django.core.files.storage.FileSystemStorage(
                    location='/home/fury/projects/cappa/public/sql_files'
                ),
                unique=True,
                upload_to=app.databases.utils.get_db_file_path,
                verbose_name='файл'
            ),
        ),
    ]
