# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-17 12:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_treeitem_leaf'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='treeitem',
            options={'verbose_name': 'элемент структуры курсов', 'verbose_name_plural': 'структура курсов'},
        ),
        migrations.AlterModelOptions(
            name='treeitemflat',
            options={'verbose_name': 'элемент списка курсов', 'verbose_name_plural': 'Список курсов'},
        ),
    ]
