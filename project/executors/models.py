# -*- coding:utf-8 -*-
import os
import json
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Доступные исполнители
PYTHON36 = 1
EXEC_TYPES = (
    (PYTHON36,  "Python 3.6"),
)
# Названия папок с html-шаблонами исполнителей
EXEC_FOLDERS = {
    PYTHON36: "python36",
}
# Типы блоков кода
STATIC = 1
COMPACT = 2
MAXIMIZED = 3

CODE_TYPES = (
    (STATIC,    "Статичный"),
    (COMPACT,   "Исполняемый"),
    (MAXIMIZED, "Исполняемый(с тестами)"),
)
# Названия html-шаблонов для каждого типа кода
CODE_TEMPLATES = {
    STATIC: "static.html",
    COMPACT: "compact.html",
    MAXIMIZED: "maximized.html",
}

# Типы запуска кода
EXECUTE = 1
CHECK_TESTS = 2

SOLUTION_TYPES = (
    (EXECUTE, "Запуск кода"),
    (CHECK_TESTS, "Запуск тестов"),
)


class Executor(models.Model):

    class Meta:
        verbose_name = "исполнитель кода"
        verbose_name_plural = "исполнители кода"

    type_id = models.IntegerField(verbose_name="тип", choices=EXEC_TYPES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        for exec_type in EXEC_TYPES:
            if exec_type[0] == self.type_id:
                return exec_type[1]
        return ""


class Code(models.Model):

    class Meta:
        verbose_name = "блок кода"
        verbose_name_plural = "блоки кода"

    type = models.IntegerField(verbose_name="тип", choices=CODE_TYPES, default=STATIC)
    executor_type_id = models.IntegerField(verbose_name="Исполнитель", null=True, blank=True, choices=EXEC_TYPES,
                                           help_text="если не выбран то наследуется")
    save_solutions = models.BooleanField(verbose_name='сохранять пользовательские решения', default=False)
    content = models.TextField(verbose_name='код', null=True, blank=True)
    content_max_signs = models.PositiveIntegerField(verbose_name="макс. символов в коде", default="1000")
    input = models.TextField(verbose_name='ввод', null=True, blank=True)
    input_max_signs = models.PositiveIntegerField(verbose_name="макс. символов на входе", default="100")
    solution = models.TextField(verbose_name='решение', null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def get_template(self):
        """ Возвращает директорию до шаблона с учетом указанного исполнителя и типа кода"""
        executor = self.executor_type_id
        if not executor:
            # если исполнитель не выбран то наследуется от связанного объекта
            try:
                obj = self.content_object
                obj_content_type = ContentType.objects.get_for_model(model=obj)
                executor_type_id = Executor.objects.get(content_type=obj_content_type.id, object_id=obj.id).type_id
            except Executor.DoesNotExist:
                # если исполнитель не выыбран для связанного объекта то использовать шаблон по умолчанию
                raise Executor.DoesNotExist("Установи исполнитель для элемента курса или блока кода")  # TODO сделать блекджековый дефолтный шаблон

            executor_folder = EXEC_FOLDERS[executor_type_id]
        else:
            executor_folder = EXEC_FOLDERS[self.executor_type_id]

        code_template = CODE_TEMPLATES[self.type]
        template = os.path.join("executors", executor_folder, code_template)
        return template

    def get_executor_type_id(self):
        if self.executor_type_id:
            return self.executor_type_id
        else:
            try:
                obj = self.content_object
                obj_content_type = ContentType.objects.get_for_model(model=obj)
                return Executor.objects.get(content_type=obj_content_type.id, object_id=obj.id).type_id
            except Executor.DoesNotExist:
                return None

    def __str__(self):
        return "#code%s#" % self.id


class CodeTest(models.Model):

    input = models.TextField(verbose_name='входные данные', null=True, blank=True)
    output = models.TextField(verbose_name='правильный ответ', null=True, blank=True)
    code = models.ForeignKey(Code, verbose_name='блок кода')
    # TODO анализатор кода для теста на javarush


class CodeSolution(models.Model):

    default_details = json.dumps({"solutions": []}, ensure_ascii=False)

    code = models.ForeignKey(Code, verbose_name="блок кода")
    user = models.ForeignKey(User, verbose_name="пользователь")
    details = models.TextField(verbose_name="детали решения", default=default_details)
    success = models.BooleanField(verbose_name="задача решена", default=False)
    execute_count = models.PositiveIntegerField(verbose_name="количество запусков кода", default=0)
    check_tests_count = models.PositiveIntegerField(verbose_name="количество запусков тестирования", default=0)

    def __str__(self):
        return "%s (%s)" % (self.user, self.code)
