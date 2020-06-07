# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-07 18:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('langs', '0003_auto_20200216_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lang',
            name='provider_name',
            field=models.CharField(choices=[('python', 'Python3'), ('cpp', 'C++'), ('csharp', 'C#')], max_length=255, unique=True, verbose_name='провайдер'),
        ),
    ]
