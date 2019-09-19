# -*- coding:utf-8 -*-
import os
import json
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from project.courses.models import TreeItem
from django.contrib.postgres.fields import JSONField, ArrayField
from django.urls import reverse


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

    def get_template(self):
        return os.path.join("executors", self.CODE_TEMPLATES[self.type])

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
            return self.treeitem.tree_name
        return "-"

    def get_order_number(self):
        if self.treeitem:
            return self.treeitem.order_number
        return '-'

    def get_author(self):
        """ Возвращает автора связанного элемента курса """
        if self.treeitem and self.treeitem.author:
            return self.treeitem.author
        return "-"

    def check_tests(self, content, input, tests):
        if self.get_executor_type_id() == Executor.PYTHON36:
            from project.executors.python36.utils import check_tests
        elif self.get_executor_type_id() == Executor.CPP:
            from project.executors.cpp.utils import check_tests
        elif self.get_executor_type_id() == Executor.CH:
            from project.executors.ch.utils import check_tests
        return check_tests(self, content, input, tests)

    def execute(self, content, input):
        if self.get_executor_type_id() == Executor.PYTHON36:
            from project.executors.python36.utils import execute_code
        elif self.get_executor_type_id() == Executor.CPP:
            from project.executors.cpp.utils import execute_code
        elif self.get_executor_type_id() == Executor.CH:
            from project.executors.ch.utils import execute_code
        return execute_code(self, content, input)


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

    class Meta:
        verbose_name = "решение"
        verbose_name_plural = "решения"

    # Статус решения
    SUCCESS = 'success'
    PROCESS = 'process'
    UNLUCK  = 'unluck'
    NONE    = 'none'

    # Типы исполнения кода
    EXECUTE = 1
    CHECK_TESTS = 2

    SOLUTION_TYPES = (
        (EXECUTE, "Запуск кода"),
        (CHECK_TESTS, "Запуск тестов"),
    )

    code = models.ForeignKey(Code, verbose_name="блок кода")
    user = models.ForeignKey(User, verbose_name="пользователь")
    last_changes = JSONField(verbose_name="последние изменения", blank=True, null=True)
    best = JSONField(verbose_name="лучшее решение", blank=True, null=True)
    versions = JSONField(verbose_name="сохраненные решения", default=list)

    details = JSONField(verbose_name="детали решения", default={})

    def __str__(self):
        return "%s (%s)" % (self.user, self.code.get_title())

    def get_formated_time(self, str_date):

        d = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S.%f')
        return d.strftime('%Y.%m.%d [%H:%M]')

    @property
    def best_time(self):
        if self.best:
            return self.get_formated_time(self.best['datetime'])
        else:
            return ''

    @property
    def progress(self):
        if self.best is None:
            return None
        else:
            return int(self.best['progress'])

    @property
    def status_success(self):
        return self.progress == 100

    @property
    def status_process(self):
        return self.progress != 100

    @property
    def status_unluck(self):
        return self.progress == 0

    @property
    def status_none(self):
        return self.best is None

    @property
    def status(self):
        if self.status_none:
            return self.NONE
        else:
            if self.status_success:
                return self.SUCCESS
            elif self.status_unluck:
                return self.UNLUCK
            else:
                return self.PROCESS

    def __create_version(self, data):

        return {
            "datetime": data['datetime'],
            "input": data.get('input', ''),
            "content": data['content'],
            "progress": data['progress'],
            "tests": {
                'num': data.get("num", ''),
                'num_success': data.get("success_num", ''),
            }
        }

    def update_best(self, data=None, version=None):
        if not version:
            version = self.__create_version(data)

        self.last_changes = version
        if self.best is None:
            self.best = version
        else:
            if int(version['progress']) > self.progress:
                self.best = version

    def add_version(self, data):
        version = self.__create_version(data)
        self.last_changes = version
        self.versions.append(json.dumps(version, ensure_ascii=False))
        self.update_best(version=version)

    def get_versions(self):
        data = []
        for json_version in self.versions:
            version = json.loads(json_version)
            version['datetime'] = self.get_formated_time(version['datetime'])
            version['content'] = {
                'name': 'content',
                'value': version['content'],
            }
            data.append(version)
        return data

    def get_absolute_url(self):
        return reverse('user_solution', kwargs={'user_id': self.user.id, 'code_id': self.code.id})
