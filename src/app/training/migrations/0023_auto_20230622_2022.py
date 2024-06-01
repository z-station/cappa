# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-06-22 20:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0022_auto_20220629_0021'),
        ('tasks', '0017_auto_20230622_1843'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='courseuserplagstatistics',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='courseuserplagstatistics',
            name='course',
        ),
        migrations.RemoveField(
            model_name='courseuserplagstatistics',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='courseuserstatistics',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='courseuserstatistics',
            name='course',
        ),
        migrations.RemoveField(
            model_name='courseuserstatistics',
            name='user',
        ),
        migrations.RemoveField(
            model_name='taskitem',
            name='task',
        ),
        migrations.RemoveField(
            model_name='taskitem',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='number',
        ),
        migrations.DeleteModel(
            name='CourseUserPlagStatistics',
        ),
        migrations.DeleteModel(
            name='CourseUserStatistics',
        ),
        migrations.DeleteModel(
            name='TaskItem',
        ),
    ]