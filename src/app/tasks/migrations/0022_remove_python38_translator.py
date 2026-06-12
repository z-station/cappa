# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0021_auto_20240703_1121'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            UPDATE tasks_taskitem
            SET translator = array_replace(translator, 'Python3.8', 'Python314')
            WHERE 'Python3.8' = ANY(translator);
        """,
            reverse_sql="""
            UPDATE tasks_taskitem
            SET translator = array_replace(translator, 'Python314', 'Python3.8')
            WHERE 'Python314' = ANY(translator);
        """,
        ),
    ]
