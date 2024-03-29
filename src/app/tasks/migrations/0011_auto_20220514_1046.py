# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-05-14 10:46
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_auto_20220420_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalSolution',
            fields=[
            ],
            options={
                'verbose_name': 'внешнее решение',
                'verbose_name_plural': 'внешние решения',
                'ordering': ('-created',),
                'proxy': True,
                'indexes': [],
            },
            bases=('tasks.solution',),
        ),
        migrations.AlterModelOptions(
            name='solution',
            options={'ordering': ('-created',), 'verbose_name': 'решение задачи', 'verbose_name_plural': 'решения задач'},
        ),
        migrations.AlterField(
            model_name='solution',
            name='description',
            field=tinymce.models.HTMLField(null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='review_status',
            field=models.CharField(choices=[('ready', 'ожидает проверки'), ('review', 'в процессе проверки'), ('checked', 'проверено')], max_length=255, null=True, verbose_name='статус'),
        ),
    ]
