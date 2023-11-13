from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.urls import reverse
from app.common.fields import OrderField


UserModel = get_user_model()


class Course(models.Model):

    class Meta:
        verbose_name = "раздел сайта"
        verbose_name_plural = "разделы сайта"
        ordering = ['order_key']

    show = models.BooleanField(verbose_name="отображать", default=True)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    slug = models.SlugField(verbose_name="слаг", max_length=255, unique=True)
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)
    about = HTMLField(verbose_name="краткое описание", default="", blank=True, null=True)
    content = HTMLField(verbose_name="текстовый контент", default="", blank=True, null=True)
    content_bottom = HTMLField(verbose_name="текстовый контент под списком страниц", default="", blank=True, null=True)
    order_key = OrderField(verbose_name='порядок', blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)

    @property
    def topics(self):
        return self._topics.filter(show=True)

    def get_breadcrumbs(self):
        return [
            {'title': 'Разделы сайта', 'url': reverse('training:courses')},
        ]

    def get_absolute_url(self):
        return reverse('training:course', kwargs={'course': self.slug})

    def __str__(self):
        return self.title
