import json
from django.core.cache import cache
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from datetime import datetime
from django.urls import reverse
from src.tasks.models import Task
from src.training.models import Topic
from src.training.fields import OrderField, SlugField


UserModel = get_user_model()


class TaskItem(models.Model):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ['order_key']

    show = models.BooleanField(verbose_name="отображать", default=True)
    task = models.ForeignKey(Task, verbose_name='задача', related_name='topics')
    slug = SlugField(verbose_name="слаг", max_length=255, blank=True, null=True, for_fields=['topic'])

    number = models.PositiveIntegerField(verbose_name='порядковый номер', blank=True, null=True)
    order_key = OrderField(verbose_name='порядок', blank=True, null=True, for_fields=['topic'])
    topic = models.ForeignKey(Topic, verbose_name='тема', related_name='_taskitems')

    @property
    def lang(self):
        return self.topic.lang

    @property
    def title(self):
        return self.task.title

    @property
    def numbered_title(self):
        data = self.get_cache_data()
        return '%s %s' % (data['number'], data['title'])

    @property
    def cache_key(self):
        return 'taskitem__%d' % self.id

    def get_data(self):
        return {
            'id': self.cache_key,
            'number': '%s.%s' % (self.topic.number, self.number),
            'title': self.title,
            'url': reverse('training:taskitem', kwargs={
                    'course': self.topic.course.slug,
                    'topic': self.topic.slug,
                    'taskitem': self.slug
                }
            )
        }

    def get_cache_data(self):
        json_data = cache.get(self.cache_key)
        if not json_data:
            data = self.get_data()
            cache.set(self.cache_key, json.dumps(data, ensure_ascii=False))
        else:
            data = json.loads(json_data)
        return data

    def get_breadcrumbs(self):
        return [
            {'title': 'Курсы', 'url': reverse('training:courses')},
            {'title': self.topic.course.title,   'url': self.topic.course.get_absolute_url()},
            {'title': self.topic.numbered_title, 'url': self.topic.get_absolute_url()},
        ]

    def get_absolute_url(self):
        return self.get_cache_data()['url']

    def __str__(self):
        return self.title


class Solution(models.Model):

    class Meta:
        verbose_name = "решение задачи"
        verbose_name_plural = "решения задач"

    class Status:
        NONE = '0'
        UNLUCK = '1'
        PROCESS = '2'
        SUCCESS = '3'
        CHOICES = (
            (NONE, 'нет попыток'),
            (UNLUCK, 'нет прогресса'),
            (PROCESS, 'есть прогресс'),
            (SUCCESS, 'решено'),
        )

    taskitem = models.ForeignKey(TaskItem, verbose_name='задача', related_name='_solution')
    user = models.ForeignKey(UserModel, verbose_name="пользователь")
    status = models.CharField(verbose_name='статус', max_length=255,  choices=Status.CHOICES, default=Status.NONE)
    progress = models.PositiveIntegerField(verbose_name='Прогресс решения', blank=True, null=True)
    last_changes = models.TextField(verbose_name="последние изменения", blank=True, default='')
    version_best = JSONField(verbose_name="лучшее решение", blank=True, null=True)
    version_list = JSONField(verbose_name="список сохраненных решений", default=list, blank=True, null=True)

    def _create_version_data(self, content, tests_result):
        if tests_result['num_success'] > 0 and tests_result['num'] > 0:
            progress = round(100 * tests_result['num_success'] / tests_result['num'])
        else:
            progress = 0
        return {
            "datetime": str(datetime.now()),
            "content": content,
            "progress": progress,
            "tests": {
                'num': tests_result['num'],
                'num_success': tests_result['num_success'],
            }
        }

    def _set_status(self):
        if self.progress is None:
            self.status = self.Status.NONE
        if self.progress == 0:
            self.status = self.Status.UNLUCK
        elif self.progress == 100:
            self.status = self.Status.SUCCESS
        else:
            self.status = self.Status.PROCESS

    def update(self, content, tests_result):
        version = self._create_version_data(content, tests_result)
        self.last_changes = content
        if self.version_best:
            if version['progress'] > self.progress:
                self.version_best = version
                self.progress = version['progress']
                self._set_status()
        else:
            self.version_best = version
            self.progress = version['progress']
            self._set_status()

    def create_version(self, content, tests_result):
        version = self._create_version_data(content, tests_result)
        self.last_changes = content
        if self.version_best:
            if version['progress'] > self.progress:
                self.version_best = version
                self.progress = version['progress']
                self._set_status()
        else:
            self.version_best = version
            self.progress = version['progress']
            self._set_status()

        if len(self.version_list) < 10:
            self.version_list.append(version)
        else:
            self.version_list[9] = version

    def get_breadcrumbs(self):
        return [
            {'title': 'Курсы', 'url': reverse('training:courses')},
            {'title': self.taskitem.topic.course.title,   'url': self.taskitem.topic.course.get_absolute_url()},
            {'title': self.taskitem.topic.numbered_title, 'url': self.taskitem.topic.get_absolute_url()},
            {'title': self.taskitem.numbered_title,       'url': self.taskitem.get_absolute_url()},
        ]

    def get_absolute_url(self):
        return reverse(
            'training:solution',
            kwargs={
                'course': self.taskitem.topic.course.slug,
                'topic': self.taskitem.topic.slug,
                'taskitem': self.taskitem.slug
            }
        )

    def __str__(self):
        return '%s: %s' % (self.user.get_full_name(), self.taskitem.title)


__all__ = ['TaskItem', 'Solution']
