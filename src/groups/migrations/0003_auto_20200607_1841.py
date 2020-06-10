# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-07 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
        ('groups', '0002_groupcourse_show_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_table', models.BooleanField(default=False, verbose_name='отображать таблицу результатов')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_quizzes', to='groups.Group')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.Quiz', verbose_name='самостоятельная работа')),
            ],
            options={
                'verbose_name': 'самостоятельная работа',
                'verbose_name_plural': 'самостоятельные работы',
            },
        ),
        migrations.AlterUniqueTogether(
            name='groupquiz',
            unique_together=set([('group', 'quiz')]),
        ),
    ]