# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-21 10:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.BooleanField(default=True, verbose_name='отображать')),
                ('title', models.CharField(max_length=255, verbose_name='название')),
                ('status', models.CharField(choices=[('0', 'открыто'), ('1', 'закрыто'), ('2', 'по кодовому слову')], default='1', max_length=255, verbose_name='вступление в группу')),
                ('codeword', models.CharField(blank=True, max_length=255, null=True, verbose_name='кодовое слово')),
                ('content', tinymce.models.HTMLField(blank=True, null=True, verbose_name='описание')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
            ],
            options={
                'verbose_name': 'учебная группа',
                'verbose_name_plural': 'учебные группы',
            },
        ),
        migrations.CreateModel(
            name='GroupCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.Course', verbose_name='курс')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_courses', to='groups.Group')),
            ],
            options={
                'verbose_name': 'учебный курс',
                'verbose_name_plural': 'учебные курсы',
            },
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to='groups.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to=settings.AUTH_USER_MODEL, verbose_name='участник')),
            ],
            options={
                'verbose_name': 'участник',
                'verbose_name_plural': 'участники',
                'ordering': ['user__last_name'],
            },
        ),
        migrations.AddField(
            model_name='group',
            name='_members',
            field=models.ManyToManyField(related_name='training_groups', through='groups.GroupMember', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AlterUniqueTogether(
            name='groupmember',
            unique_together=set([('group', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupcourse',
            unique_together=set([('group', 'course')]),
        ),
    ]
