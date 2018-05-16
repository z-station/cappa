# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.cache import cache
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from tinymce.models import HTMLField
from django.contrib.auth.models import User


class TreeItem(MPTTModel):

    class Meta:
        verbose_name = "Элемент курса"
        verbose_name_plural = "Элементы курса"

    parent = TreeForeignKey(
        'self',
        related_name='children',
        editable=False,
        on_delete=models.CASCADE,
        verbose_name="Родительский элемент",
        null=True, blank=True,
    )

    leaf = False
    show = models.BooleanField(verbose_name="Отображать", default=True)
    last_modified = models.DateTimeField(verbose_name="Дата последнего изменения", auto_now=True)
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="url", unique=True, max_length=255)
    long_title = models.CharField(max_length=255, verbose_name="Длинный заголовок", blank=True, null=True)
    about = HTMLField(verbose_name="Описание", default="", blank=True, null=True)
    content = HTMLField(verbose_name="Содержимое", default="", blank=True, null=True)
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    def cache_url_key(self):
        """Возвращает ключ  в cache на url TreeItem """
        return 'treeitem_%d_url' % self.id

    def clear_cache(self):
        """ очистка cache при удалении элемента
        (очищается информация у элемента и его дочерних элементов)"""
        cache.delete(self.cache_url_key())
        for child in self.get_children():
            child.clear_cache()

    def get_complete_slug(self):
        """
        :return: full url of object.
        """
        """если имеется url в cache то возвращаем url, 
        иначе встраиваем url от листьев к корню дерва
         ex.: course/topic/task"""
        key = self.cache_url_key()
        url = cache.get(key, None)
        if url is None:
            url = self.slug
            if not self.is_root_node():
                for ancestor in self.get_ancestors(ascending=True):
                    url = ancestor.slug + '/' + url
            cache.set(key, url, None)
        return url

    def get_absolute_url(self):
        """Для получения url текущего элемента используется метод get_complete_slug см.выше  """
        path = self.get_complete_slug()
        return reverse('courses-item', kwargs={'path': path})



    def move_to(self, target, position='first-child'):
        """
        Clear cache when moving
        """
        self.clear_cache()
        super(TreeItem, self).move_to(target, position=position)

