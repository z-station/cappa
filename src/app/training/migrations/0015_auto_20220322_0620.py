# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-03-22 06:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0014_create_tokens'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='solution',
            options={'ordering': ('-last_modified',), 'verbose_name': 'решение задачи', 'verbose_name_plural': 'решения задач'},
        ),
        migrations.AddField(
            model_name='solution',
            name='translator',
            field=models.CharField(choices=[('Python3.8', 'Python3.8'), ('GCC7.4', 'GCC7.4'), ('Prolog-D', 'Prolog-D')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='translator',
            field=models.CharField(choices=[('Python3.8', 'Python 3.8'), ('GCC7.4', 'С++ (GCC 7.4)'), ('Prolog-D', 'Пролог-Д')], max_length=100, verbose_name='транслятор кода'),
        ),
        migrations.RunSQL(sql="""
            UPDATE training_course 
            SET translator = CASE
              WHEN translator = '1' THEN 'Python3.8'
              WHEN translator = '2' THEN 'GCC7.4'
            END
        """),
        migrations.RunSQL(sql="""
            UPDATE training_solution ts
            SET translator = (
               SELECT tc.translator
               FROM training_taskitem tti 
                 INNER JOIN training_topic tt ON tti.topic_id = tt.id
                 INNER JOIN training_course tc ON tt.course_id = tc.id
               WHERE ts.taskitem_id = tti.id
            )
        """)
    ]