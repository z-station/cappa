from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.urls import reverse
from app.training.models import Course
from app.common.fields import OrderField


UserModel = get_user_model()


class Topic(models.Model):

    class Meta:
        verbose_name = "страница"
        verbose_name_plural = "страницы"
        ordering = ['order_key']

    show = models.BooleanField(verbose_name="отображать", default=True)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    slug = models.SlugField(verbose_name="слаг", max_length=255)
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)

    course = models.ForeignKey(Course, verbose_name='курс', related_name='_topics')
    order_key = OrderField(verbose_name='порядок', blank=True,  null=True, for_fields=['course'])
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)

    def get_breadcrumbs(self):
        return [
            {'title': 'Разделы сайта', 'url': reverse('training:courses')},
            {'title': self.course.title, 'url': self.course.get_absolute_url()},
        ]

    def get_absolute_url(self):
        return reverse(
            'training:topic',  kwargs={
                'course': self.course.slug,
                'topic': self.slug
            }
        )

    def __str__(self):
        return self.title


class Content(models.Model):

    class Meta:
        verbose_name = "блок контента"
        verbose_name_plural = "блоки контента"
        ordering = ['order_key']

    ACE = 'ace'
    TEXT = 'text'
    CHOICES = (
        (ACE, 'код'),
        (TEXT, 'текст'),
    )

    input = models.TextField(verbose_name='Консольный ввод', blank=True, null=True)
    content = models.TextField(verbose_name='Редактор', blank=True, null=True)
    text = HTMLField(blank=True, null=True)
    type = models.CharField(verbose_name='тип', max_length=255, choices=CHOICES, default='text')
    topic = models.ForeignKey(Topic, related_name='_content')
    order_key = OrderField(verbose_name='порядок', blank=True, for_fields=['topic'])


__all__ = ['Course', 'Topic', 'Content']
