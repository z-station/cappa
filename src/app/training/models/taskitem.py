import json
from django.core.cache import cache
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from app.tasks.models import Task
from app.tasks.enums import ScoreMethod
from app.training.models import Topic
from app.translators.enums import TranslatorType
from app.common.fields import OrderField, SlugField

UserModel = get_user_model()


class TaskItem(models.Model):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ['order_key']

    show = models.BooleanField(verbose_name="отображать", default=True)
    task = models.ForeignKey(Task, verbose_name='задача', related_name='topics')
    max_score = models.PositiveIntegerField(verbose_name='балл за решение', default=5)
    score_method = models.CharField(
        verbose_name='метод оценивания',
        max_length=50,
        choices=ScoreMethod.CHOICES,
        default=ScoreMethod.TESTS
    )
    slug = SlugField(verbose_name="слаг", max_length=255, blank=True, null=True, for_fields=['topic'])

    number = models.PositiveIntegerField(verbose_name='порядковый номер', blank=True, null=True)
    order_key = OrderField(verbose_name='порядок', blank=True, null=True, for_fields=['topic'])
    topic = models.ForeignKey(Topic, verbose_name='тема', related_name='_taskitems')

    @property
    def translator(self) -> int:
        return self.topic.translator

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
        return 'taskitem__%d' % self.id

    def get_data(self):
        return {
            'id': self.id,
            'number': '%s.%s' % (self.topic.number, self.number),
            'title': self.title,
            'task_id': self.task_id,
            'url': reverse(
                'training:taskitem',
                kwargs={
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

    def score_method_is_tests(self):
        return self.score_method == ScoreMethod.TESTS

    def score_method_is_review(self):
        return self.score_method == ScoreMethod.REVIEW

    def score_method_is_tests_and_review(self):
        return self.score_method == ScoreMethod.TESTS_AND_REVIEW

    def __str__(self):
        return self.title

