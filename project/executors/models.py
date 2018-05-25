# -*- coding:utf-8 -*-
import os
import json
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Executor(models.Model):

    # Доступные исполнители
    PYTHON36 = 1
    EXEC_TYPES = (
        (PYTHON36,  "Python 3.6"),
    )
    # Названия папок с html-шаблонами исполнителей
    EXEC_FOLDERS = {
        PYTHON36: "python36",
    }

    class Meta:
        verbose_name = "исполнитель кода"
        verbose_name_plural = "исполнители кода"

    type_id = models.IntegerField(verbose_name="тип", choices=EXEC_TYPES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        for exec_type in self.EXEC_TYPES:
            if exec_type[0] == self.type_id:
                return exec_type[1]
        return ""


class Code(models.Model):

    # Типы блоков кода
    STATIC = 1
    EXECUTABLE = 2

    CODE_TYPES = (
        (STATIC,    "Статичный"),
        (EXECUTABLE, "Исполняемый"),
    )
    # Названия html-шаблонов для каждого типа кода
    CODE_TEMPLATES = {
        STATIC: "static.html",
        EXECUTABLE: "executable.html",
    }

    class Meta:
        verbose_name = "блок кода"
        verbose_name_plural = "блоки кода"

    type = models.IntegerField(verbose_name="тип", choices=CODE_TYPES, default=STATIC)
    executor_type_id = models.IntegerField(verbose_name="Исполнитель", null=True, blank=True, choices=Executor.EXEC_TYPES,
                                           help_text="если не выбран то наследуется")
    content = models.TextField(verbose_name='код', null=True, blank=True)
    input = models.TextField(verbose_name='ввод', null=True, blank=True)
    solution = models.TextField(verbose_name='эталонное решение', null=True, blank=True)

    show_input = models.BooleanField(verbose_name='отображать блок ввода', default=False)
    show_tests = models.BooleanField(verbose_name='отображать блок тестов', default=False)
    input_max_signs = models.PositiveIntegerField(verbose_name="макс. символов в блоке ввода", default=100)
    content_max_signs = models.PositiveIntegerField(verbose_name="макс. символов в блоке кода", default=1000)
    save_solutions = models.BooleanField(verbose_name='сохранять пользовательские решения', default=False)
    timeout = models.PositiveIntegerField(verbose_name="макс. время исполнения(секунд)", default=30)

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

            executor_folder = Executor.EXEC_FOLDERS[executor_type_id]
        else:
            executor_folder = Executor.EXEC_FOLDERS[self.executor_type_id]

        code_template = self.CODE_TEMPLATES[self.type]
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

    def get_title(self):
        return self.content_object.__str__()


class CodeTest(models.Model):

    class Meta:
        verbose_name = "тест"
        verbose_name_plural = "тесты"

    input = models.TextField(verbose_name='входные данные', null=True, blank=True)
    output = models.TextField(verbose_name='правильный ответ', null=True, blank=True)
    code = models.ForeignKey(Code, verbose_name='блок кода')

    def __str__(self):
        return "test %s" % self.id


class CodeSolution(models.Model):

    class Meta:
        verbose_name = "пользовательское решение"
        verbose_name_plural = "пользовательские решения"

    # Типы исполнения кода
    EXECUTE = 1
    CHECK_TESTS = 2

    SOLUTION_TYPES = (
        (EXECUTE, "Запуск кода"),
        (CHECK_TESTS, "Запуск тестов"),
    )

    default_details = json.dumps({"solutions": []}, ensure_ascii=False)

    code = models.ForeignKey(Code, verbose_name="блок кода")
    user = models.ForeignKey(User, verbose_name="пользователь")
    details = models.TextField(verbose_name="детали решения", default=default_details)
    success = models.BooleanField(verbose_name="задача решена", default=False)
    execute_count = models.PositiveIntegerField(verbose_name="количество запусков кода", default=0)
    check_tests_count = models.PositiveIntegerField(verbose_name="количество запусков тестирования", default=0)

    def __str__(self):
        return "%s (%s)" % (self.user, self.code.get_title())
