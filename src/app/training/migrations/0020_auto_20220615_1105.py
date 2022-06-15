# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-06-15 11:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0002_auto_20220615_1105'),
        ('training', '0019_auto_20220514_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='database',
            field=models.ForeignKey(help_text='обязательна для курсов по базам данных', null=True, on_delete=django.db.models.deletion.SET_NULL, to='databases.Database', verbose_name='учебная база данных'),
        ),
        migrations.AlterField(
            model_name='course',
            name='translator',
            field=models.CharField(choices=[('Python3.8', 'Python 3.8'), ('GCC7.4', 'С++ (GCC 7.4)'), ('Prolog-D', 'Пролог-Д'), ('PostgreSQL', 'PostgreSQL 13'), ('Pascal', 'PascalABC.NET')], max_length=100, verbose_name='транслятор кода'),
        ),
    ]
