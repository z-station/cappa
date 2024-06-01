# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-06-19 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_task_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='rating_is_calculated',
            field=models.BooleanField(default=False, verbose_name='решение учтено в рейтинге'),
        ),
        migrations.AddField(
            model_name='task',
            name='rating_success',
            field=models.PositiveIntegerField(default=0, verbose_name='количество успешных решений'),
        ),
        migrations.AddField(
            model_name='task',
            name='rating_total',
            field=models.PositiveIntegerField(default=0, verbose_name='количество решений'),
        ),
    ]