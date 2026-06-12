# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models



class Migration(migrations.Migration):

    dependencies = [
        ('training', '0023_auto_20230622_2022'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                UPDATE training_course
                SET translator = 'Python314'
                WHERE translator = 'Python3.8';
            """,
        ),
    ]
