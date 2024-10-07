import json
from typing import Optional
from django.core.cache import cache
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from app.tasks.models import Task
from app.tasks.enums import ScoreMethod, TaskItemType
from app.tasks.querysets import TaskItemQuerySet
from app.translators.enums import TranslatorType
from app.common.fields import OrderField, TaskItemSlugField
from app.databases.models import Database


UserModel = get_user_model()


class TaskItem(models.Model):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ['order_key']

    show = models.BooleanField(
        verbose_name="отображать",
        default=True
    )
    type = models.CharField(
        verbose_name='источник задачи',
        choices=TaskItemType.CHOICES,
        max_length=100
    )
    topic = models.ForeignKey(
        'training.Topic',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='taskitems'
    )
    task = models.ForeignKey(
        Task,
        verbose_name='задача',
        related_name='taskitems'
    )
    max_score = models.PositiveIntegerField(
        verbose_name='балл за решение',
        default=5
    )
    score_method = models.CharField(
        verbose_name='метод оценивания',
        max_length=50,
        choices=ScoreMethod.CHOICES,
        default=ScoreMethod.TESTS
    )
    slug = TaskItemSlugField(
        verbose_name="слаг",
        max_length=255,
        blank=True,
        null=True,
        for_fields=['topic']
    )
    order_key = OrderField(
        verbose_name='порядковый номер',
        blank=True,
        null=True,
        for_fields=['topic']
    )
    translator = ArrayField(
        verbose_name='транслятор кода',
        base_field=models.CharField(
            choices=TranslatorType.CHOICES,
            max_length=10000
        ),
    )
    database = models.ForeignKey(
        Database,
        verbose_name='учебная база данных',
        help_text='обязательна для задач по базам данных',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    objects = TaskItemQuerySet.as_manager()

    @property
    def translator_name(self) -> str:
        return TranslatorType.MAP[self.translator]

    @property
    def title(self):
        return self.task.title

    @property
    def numbered_title(self):
        data = self.get_cache_data()
        return '%s %s' % (data['number'], data['title'])

    @property
    def cache_key(self):
        return f'taskitem__{self.id}'

    @property
    def type_course(self):
        return self.type == TaskItemType.COURSE

    def get_data(self):
        if self.type == TaskItemType.COURSE:
            number = '%s.%s' % (self.topic.order_key, self.order_key)
            url = reverse(
                'training:taskitem',
                kwargs={
                    'course': self.topic.course.slug,
                    'topic': self.topic.slug,
                    'taskitem': self.slug
                }
            )
            breadcrumbs = [
                {
                    'title': 'Курсы',
                    'url': reverse('training:courses')
                },
                {
                    'title': self.topic.course.title,
                    'url': reverse(
                        'training:course',
                        kwargs={'course': self.topic.course.slug}
                    )
                },
                {
                    'title': self.topic.numbered_title,
                    'url': reverse(
                        'training:topic', kwargs={
                            'course': self.topic.course.slug,
                            'topic': self.topic.slug
                        }
                    )
                },
            ]
        elif self.type == TaskItemType.TASKBOOK:
            number = self.order_key
            url = reverse(
                'taskbook:taskitem',
                kwargs={'taskitem': self.slug}
            )
            breadcrumbs = [
                {
                    'title': 'Задачник',
                    'url': reverse('taskbook:taskbook')
                },
            ]
        else:
            number = self.order_key
            url = None
            breadcrumbs = None
        return {
            'id': self.id,
            'number': number,
            'title': self.title,
            'task_id': self.task_id,
            'breadcrumbs': breadcrumbs,
            'url': url,
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
        return self.get_cache_data()['breadcrumbs']

    def get_absolute_url(self):
        return self.get_cache_data()['url']

    def get_db_name(self) -> Optional[str]:
        return self.database.db_name if self.database else None

    @property
    def score_method_is_tests(self):
        return self.score_method == ScoreMethod.TESTS

    @property
    def score_method_is_review(self):
        return self.score_method == ScoreMethod.REVIEW

    @property
    def score_method_is_tests_and_review(self):
        return self.score_method == ScoreMethod.TESTS_AND_REVIEW

    @property
    def score_method_with_tests(self):
        return self.score_method in ScoreMethod.TESTS_METHODS

    def __str__(self):
        return self.title

