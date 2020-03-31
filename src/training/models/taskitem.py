import json
from django.core.cache import cache
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from tinymce.models import HTMLField
from datetime import datetime
from django.urls import reverse
from src.tasks.models import Task
from src.training.models import Topic
from src.utils.fields import OrderField, SlugField


UserModel = get_user_model()


class TaskItem(models.Model):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ['order_key']

    show = models.BooleanField(verbose_name="отображать", default=True)
    task = models.ForeignKey(Task, verbose_name='задача', related_name='topics')
    max_score = models.PositiveIntegerField(verbose_name='балл за решение', default=5)
    manual_check = models.BooleanField(verbose_name='ручная проверка', default=False)
    compiler_check = models.BooleanField(verbose_name='проверка автотестами', default=True)
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

    MS__NOT_CHECKED = '0'
    MS__READY_TO_CHECK = '1'
    MS__CHECK_IN_PROGRESS = '2'
    MS__CHECKED = '3'
    MS__BLOCKED_STATUSES = (MS__READY_TO_CHECK, MS__CHECK_IN_PROGRESS, MS__CHECKED)
    MS__AWAITING_CHECK = (MS__READY_TO_CHECK, MS__CHECK_IN_PROGRESS)
    MS__CHOICES = (
        (MS__NOT_CHECKED, 'нет'),
        (MS__READY_TO_CHECK, 'ожидает проверки'),
        (MS__CHECK_IN_PROGRESS, 'в процессе проверки'),
        (MS__CHECKED, 'проверено'),
    )

    S__NONE = '0'
    S__UNLUCK = '1'
    S__IN_PROGRESS = '2'
    S__SUCCESS = '3'
    S__CHOICES = (
        (S__NONE, 'нет попыток'),
        (S__UNLUCK, 'нет решения'),
        (S__IN_PROGRESS, 'частично решено'),
        (S__SUCCESS, 'решено'),
    )

    taskitem = models.ForeignKey(TaskItem, verbose_name='задача', related_name='_solution')
    user = models.ForeignKey(UserModel, verbose_name="пользователь")
    manual_status = models.CharField(
        verbose_name='статус проверки преподавателем', max_length=255,
        choices=MS__CHOICES, default=MS__NOT_CHECKED
    )
    tests_score = models.FloatField(verbose_name='оценка по автотестам', blank=True, null=True)
    manual_score = models.FloatField(verbose_name='оценка преподавателя', blank=True, null=True)
    last_changes = models.TextField(verbose_name="последние изменения", blank=True, default='')
    version_best = JSONField(verbose_name="лучшее решение", blank=True, null=True)
    version_list = JSONField(verbose_name="список сохраненных решений", default=list, blank=True, null=True)
    comment = HTMLField(verbose_name="комментарий к решению", blank=True, null=True)

    @property
    def score(self):

        """ Оценка преподавателя имеет больший приоритет чем оценка по автотестам """

        if self.taskitem.manual_check:
            if self.manual_status == self.MS__CHECKED:
                return self.manual_score
            else:
                return None
        else:
            return self.tests_score

    @property
    def status(self) -> str:

        """ Статус вычисляется на основе оценки """

        if self.score is None:
            return self.S__NONE
        elif self.score <= 0:
            return self.S__UNLUCK
        elif self.score >= self.taskitem.max_score:
            return self.S__SUCCESS
        else:
            return self.S__IN_PROGRESS

    @property
    def status_name(self) -> str:
        """ Возващает текст статуса """
        status = self.status
        for choice in self.S__CHOICES:
            if choice[0] == status:
                return choice[1]

    @property
    def manual_status_name(self):
        for choice in self.MS__CHOICES:
            if choice[0] == self.manual_status:
                return choice[1]

    @staticmethod
    def _get_version_data(content: str, tests_score=None) -> dict:
        """ Возвращает структуру версии решения для хранения в JSON"""
        return {
            "datetime": str(datetime.now()),
            "content": content,
            "tests_score": tests_score,
        }

    def update(self, content, tests_score=None):
        self.last_changes = content
        if self.manual_status not in self.MS__BLOCKED_STATUSES:
            version = self._get_version_data(content=content, tests_score=tests_score)
            self.version_best = version
            self.tests_score = version['tests_score']

    def create_version(self, content, tests_score=None):
        version = self._get_version_data(content=content, tests_score=tests_score)
        if len(self.version_list) == 10:
            self.version_list.pop(0)
        self.version_list.append(version)

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

    def __repr__(self):
        return f"Solution: {self.__str__()}"


__all__ = ['TaskItem', 'Solution']
