# -*- coding:utf-8 -*-
import os
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Доступные исполнители
PYTHON36 = 1
EXECUTORS_NAMES = (
    (PYTHON36,  "Python 3.6"),
)
# Названия папок с html-шаблонами исполнителей
EXECUTORS_FOLDERS = {
    PYTHON36: "python36",
}
# Типы блоков кода
STATIC = 1
COMPACT = 2
MAXIMIZED = 3

CODE_TYPES = (
    (STATIC,    "Статичный"),
    (COMPACT,   "Исполняемый(компактный)"),
    (MAXIMIZED, "Исполняемый"),
)
# Названия html-шаблонов для каждого типа кода
CODE_TEMPLATES = {
    STATIC: "static.html",
    COMPACT: "compact.html",
    MAXIMIZED: "maximized.html",
}


class Executor(models.Model):

    class Meta:
        verbose_name = "исполнитель кода"
        verbose_name_plural = "исполнители кода"

    name = models.IntegerField(verbose_name="название", choices=EXECUTORS_NAMES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        for name in EXECUTORS_NAMES:
            if name[0] == self.name:
                return name[1]
        return ""


class Code(models.Model):

    class Meta:
        verbose_name = "блок кода"
        verbose_name_plural = "блоки кода"

    type = models.IntegerField(verbose_name="тип", choices=CODE_TYPES, default=STATIC)
    executor = models.IntegerField(verbose_name="Исполнитель", null=True, blank=True, choices=EXECUTORS_NAMES,
                                   help_text="если не выбран то наследуется")
    content = models.TextField(verbose_name='код', null=True, blank=True)
    input = models.TextField(verbose_name='ввод', null=True, blank=True)
    output = models.TextField(verbose_name='вывод', null=True, blank=True)
    solution = models.TextField(verbose_name='решение', null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def get_template(self):
        """ Возвращает директорию до шаблона с учетом указанного исполнителя и типа кода"""
        executor = self.executor
        if not executor:
            # если исполнитель не выбран то наследуется от связанного объекта
            try:
                obj = self.content_object
                obj_content_type = ContentType.objects.get_for_model(model=obj)
                executor = Executor.objects.get(content_type=obj_content_type.id, object_id=obj.id).name
            except Executor.DoesNotExist:
                # если исполнитель не выыбран для связанного объекта то использовать шаблон по умолчанию
                raise Executor.DoesNotExist  # TODO сделать блекджековый дефолтный шаблон

        executor_folder = EXECUTORS_FOLDERS[executor]
        code_template = CODE_TEMPLATES[self.type]
        template = os.path.join("executors", executor_folder, code_template)
        return template

    def __str__(self):
        return "#code%s#" % self.id
