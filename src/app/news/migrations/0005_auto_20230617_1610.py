# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-06-17 16:10
from __future__ import unicode_literals

from django.db import migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20210720_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=filebrowser.fields.FileBrowseField(blank=True, max_length=100, null=True, verbose_name='изображение'),
        ),
    ]
