# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-28 06:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20200411_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutionexample',
            name='lang',
            field=models.CharField(blank=True, choices=[('python', 'Python3'), ('cpp', 'C++'), ('csharp', 'C#'), ('php', 'PHP')], max_length=255, null=True, verbose_name='язык'),
        ),
        migrations.AlterField(
            model_name='task',
            name='lang',
            field=models.CharField(blank=True, choices=[('python', 'Python3'), ('cpp', 'C++'), ('csharp', 'C#'), ('php', 'PHP')], max_length=255, null=True, verbose_name='язык'),
        ),
        migrations.AlterField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='tasks.Tag', verbose_name='метки'),
        ),
    ]
