# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from tinymce.models import HTMLField
from django.contrib.auth.models import User


class TreeItem(MPTTModel):

    class Meta:
        verbose_name = "элемент"
        verbose_name_plural = "структура курсов"

    parent = TreeForeignKey(
        'self',
        related_name='children',
        editable=False,
        on_delete=models.CASCADE,
        verbose_name="родительский элемент",
        null=True, blank=True,
    )

    leaf = models.BooleanField(verbose_name="задача", default=False)  # leaf - это лист дерева, задача яввляется листом
    show = models.BooleanField(verbose_name="отображать", default=True)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)
    title = models.CharField(max_length=255, verbose_name="заголовок")
    slug = models.SlugField(verbose_name="слаг", max_length=255)
    long_title = models.CharField(max_length=255, verbose_name="длинный заголовок", blank=True, null=True)
    about = HTMLField(verbose_name="описание", default="", blank=True, null=True)
    content = HTMLField(verbose_name="содержимое", default="", blank=True, null=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        """ Строковое представление """
        return self.title

    def cache_url_key(self):
        """ Возвращает ключ  в cache на url TreeItem """
        return 'treeitem_%d_url' % self.id

    def clear_cache(self):
        """ Очистка cache при удалении элемента
        (очищается информация у элемента и его дочерних элементов)"""
        cache.delete(self.cache_url_key())
        for child in self.get_children():
            child.clear_cache()

    @classmethod
    def check_slug(self, target, position, slug, node):
        """ Проверяет уникальность слага на данном уровне дерева
            Если слаг уникальный возвращает True
            используется при переносе элемента по дереву """
        if target is None:
            siblings = TreeItem.objects.root_nodes()
        else:
            if position == 'first-child' or position == 'last-child':
                siblings = target.get_children()
            else:
                siblings = target.get_siblings(include_self=True)
        for sibling in siblings:
            if sibling != node and sibling.slug == slug:
                return False
        return True

    def get_complete_slug(self):
        """ Если имеется url в cache то возвращаем url,
           иначе встраиваем url от листьев к корню дерва
           ex.: course/topic/task """
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
        """ Для получения url текущего элемента используется метод get_complete_slug см.выше """
        path = self.get_complete_slug()
        return reverse('courses-item', kwargs={'path': path})

    def move_to(self, target, position='first-child'):
        """ Очистка кеша после передвижения по дереву """
        self.clear_cache()
        super(TreeItem, self).move_to(target, position=position)


class TreeItemFlat(TreeItem):
    """ Класс с расширенными правами в админ интерфейсе
        выводит список всех элементов treeitem (для администрирования)"""
    class Meta:
        proxy = True
        verbose_name = 'элемент'
        verbose_name_plural = 'Список курсов'
