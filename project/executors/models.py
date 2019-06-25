# -*- coding:utf-8 -*-
import os
import json
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from project.courses.models import TreeItem
from django.contrib.postgres.fields import JSONField


class Executor(models.Model):

    # Доступные исполнители
    PYTHON36 = 1
    CPP = 2
    CH = 3
    EXEC_TYPES = (
        (PYTHON36,  "Python 3.6"),
        (CPP,  "C++"),
        (CH,  "C#"),
    )
    # Названия папок с html-шаблонами исполнителей
    EXEC_FOLDERS = {
        PYTHON36: "python36",
        CPP: "cpp",
        CH: "ch",
    }

    class Meta:
        verbose_name = "исполнитель кода"
        verbose_name_plural = "исполнители кода"

    type_id = models.IntegerField(verbose_name="тип", choices=EXEC_TYPES)
    treeitem = models.ForeignKey(TreeItem, on_delete=models.CASCADE)

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

    type = models.IntegerField(verbose_name="тип", choices=CODE_TYPES, default=EXECUTABLE)
    executor_type_id = models.IntegerField(verbose_name="Исполнитель", null=True, blank=True, choices=Executor.EXEC_TYPES,
                                           help_text="если не выбран то наследуется", default=Executor.PYTHON36)
    treeitem = models.ForeignKey(TreeItem, verbose_name='элемент курса', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(verbose_name="описание", blank=True, null=True)

    content = models.TextField(verbose_name='код', null=True, blank=True)
    input = models.TextField(verbose_name='ввод', null=True, blank=True)
    solution = models.TextField(verbose_name='эталонное решение', null=True, blank=True)

    show_input = models.BooleanField(verbose_name='отображать блок ввода', default=False)
    show_tests = models.BooleanField(verbose_name='отображать блок тестов', default=False)
    save_solutions = models.BooleanField(verbose_name='сохранять пользовательские решения', default=False)
    input_max_signs = models.PositiveIntegerField(verbose_name="макс. символов в блоке ввода", default=100)
    content_max_signs = models.PositiveIntegerField(verbose_name="макс. символов в блоке кода", default=1000)
    timeout = models.PositiveIntegerField(verbose_name="макс. время исполнения(секунд)", default=30)

    def get_template(self, template_name=None):
        """ Возвращает полную директорию до шаблона (с учетом исполнителя)
            если указан template_name - возвращает путь до этого шаблона
            иначе возвращает путь до шаблона блока кода с указаным типом """

        executor_type_id = self.get_executor_type_id()
        executor_folder = Executor.EXEC_FOLDERS[executor_type_id]
        if template_name:
            template = os.path.join("executors", executor_folder, template_name)
        else:
            code_template = self.CODE_TEMPLATES[self.type]
            template = os.path.join("executors", executor_folder, code_template)
        return template

    def get_executor_type_id(self):
        """ Возвращает type_id исплнителя кода, иначе None """
        if self.executor_type_id:
            return self.executor_type_id
        else:
            try:
                return Executor.objects.get(treeitem=self.treeitem).type_id
            except Executor.DoesNotExist:
                raise Executor.DoesNotExist("Установите исполнитель кода для элемента курса или блока кода")  # TODO сделать блекджековый дефолтный шаблон

    def get_executor_name(self):
        executor_type_id = self.get_executor_type_id()
        for exec_type in Executor.EXEC_TYPES:
            if exec_type[0] == executor_type_id:
                return exec_type[1]

    def __str__(self):
        """ Строкове представление """
        return "#code%s#" % self.id

    def get_title(self):
        """ Возвращает title связанного элемента курса """
        if self.treeitem:
            return self.treeitem.__str__()
        return "-"

    def get_author(self):
        """ Возвращает автора связанного элемента курса """
        if self.treeitem and self.treeitem.author:
            return self.treeitem.author
        return "-"


class CodeFlat(Code):
    """ Класс с расширенными правами в админ интерфейсе (для администрирования) """
    class Meta:
        proxy = True
        verbose_name = "элемент списка блоков кода"
        verbose_name_plural = "список блоков кода"


class CodeTest(models.Model):

    class Meta:
        verbose_name = "тест"
        verbose_name_plural = "тесты"

    input = models.TextField(verbose_name='входные данные', null=True, blank=True)
    output = models.TextField(verbose_name='правильный ответ', null=True, blank=True)
    code = models.ForeignKey(Code, verbose_name='блок кода')

    def __str__(self):
        return "test %s" % self.id


class UserSolution(models.Model):
    """ """
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

    default_details = {
        "solutions": [],
        "best_solution_tests": [],
        "best_solution_num": False,
    }

    code = models.ForeignKey(Code, verbose_name="блок кода")
    user = models.ForeignKey(User, verbose_name="пользователь")
    details = JSONField(verbose_name="детали решения", default=default_details)
    progress = models.PositiveIntegerField(verbose_name="Прогресс решения", default=0)

    def __str__(self):
        return "%s (%s)" % (self.user, self.code.get_title())

    def get_template(self):
        """ Возвращает директорию до шаблона с учетом указанного исполнителя"""
        executor = self.code.executor_type_id
        if not executor:
            # если исполнитель не выбран то наследуется от связанного объекта
            try:
                executor_type_id = Executor.objects.get(treeitem=self.treeitem).type_id
            except Executor.DoesNotExist:
                # если исполнитель не выыбран для связанного объекта то использовать шаблон по умолчанию
                raise Executor.DoesNotExist("Установите исполнитель кода для элемента курса или блока кода")  # TODO сделать блекджековый дефолтный шаблон

            executor_folder = Executor.EXEC_FOLDERS[executor_type_id]
        else:
            executor_folder = Executor.EXEC_FOLDERS[self.executor_type_id]

        code_template = self.CODE_TEMPLATES[self.type]
        template = os.path.join("executors", executor_folder, code_template)
        return template

    """ Пример JSON структуры поля details
    details = {
        best_solution_num: <int>  # порядковый номер удачного решения в списке решений solutions
        best_solution_tests: [
            {"1": True},
            {"2": False},
            {...},
        ]
        solutions: [
            {
                datetime: <datetime>,  # дата/время попытки
                content:  <unicode>,   # код программы
                tests_num: <int>
                tests_success_num: <int>
            },
            {...},
            {...},
        ]
    }

    """