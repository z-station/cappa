import json
from django.core.cache import cache
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.urls import reverse
from src.training.models import Course
from src.utils.fields import OrderField


UserModel = get_user_model()


class Topic(models.Model):

    class Meta:
        verbose_name = "тема"
        verbose_name_plural = "темы"
        ordering = ['order_key']

    show = models.BooleanField(verbose_name="отображать", default=True)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    slug = models.SlugField(verbose_name="слаг", max_length=255)
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)
    end_time = models.DateTimeField(
        verbose_name="дата/время окончения решения задач в формате UTC",
        blank=True, null=True
    )

    course = models.ForeignKey(Course, verbose_name='курс', related_name='_topics')
    number = models.PositiveIntegerField(verbose_name='порядковый номер', blank=True, null=True)
    order_key = OrderField(verbose_name='порядок', blank=True,  null=True, for_fields=['course'])
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)

    @property
    def lang(self):
        return self.course.lang

    @property
    def taskitems(self):
        return self._taskitems.filter(show=True)

    @property
    def numbered_title(self):
        return '%s %s' % (self.number, self.title)

    @property
    def cache_key(self):
        return 'topic__%d' % self.id

    def get_data(self):
        return {
            'id': self.cache_key,
            'number': self.number,
            'title': self.title,
            'url': reverse(
                'training:topic',  kwargs={'course': self.course.slug, 'topic': self.slug}
            ),
            'taskitems': [taskitem.get_data() for taskitem in self.taskitems],
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
            {'title': self.course.title, 'url': self.course.get_absolute_url()},
        ]

    def get_absolute_url(self):
        return self.get_cache_data()['url']

    def __str__(self):
        return self.title


class Content(models.Model):

    class Meta:
        verbose_name = "блок контента"
        verbose_name_plural = "блоки контента"
        ordering = ['order_key']

    ACE  = 'ace'
    TEXT = 'text'
    CHOICES = (
        (ACE, 'код'),
        (TEXT, 'текст'),
    )

    input = models.TextField(verbose_name='Консольный ввод', blank=True, null=True)
    content = models.TextField(verbose_name='Редактор', blank=True, null=True)
    show_input = models.BooleanField(verbose_name='Отображать консольный ввод', default=False)
    show_debug = models.BooleanField(verbose_name='Отображать отладчик', default=True)
    readonly = models.BooleanField(verbose_name='Только для чтения', default=False)
    text = HTMLField(blank=True, null=True)
    type = models.CharField(verbose_name='тип', max_length=255, choices=CHOICES, default='text')
    topic = models.ForeignKey(Topic, related_name='_content')
    order_key = OrderField(verbose_name='порядок', blank=True, for_fields=['topic'])

    @property
    def lang(self):
        return self.topic.course.lang


__all__ = ['Course', 'Topic', 'Content']
