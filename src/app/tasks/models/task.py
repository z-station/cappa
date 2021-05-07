from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DateTimeField,
    TextField,
    PositiveIntegerField,
    BooleanField,
    ManyToManyField,
    SET_NULL
)
from django.contrib.postgres.fields import JSONField
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from app.translators.consts import Translator
from app.tasks.consts import Complexity, Checker

UserModel = get_user_model()


class Source(Model):

    class Meta:
        verbose_name = "источник"
        verbose_name_plural = "источники"
        ordering = ('name',)

    name = CharField(verbose_name="имя", max_length=255)
    description = TextField(verbose_name="описание", blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(Model):

    class Meta:
        verbose_name = "метка"
        verbose_name_plural = "метки"
        ordering = ('name',)

    name = CharField(verbose_name="имя", max_length=255)

    def __str__(self):
        return self.name


class Task(Model):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ('order_key',)

    order_key = PositiveIntegerField(verbose_name='порядок', default=0)
    title = CharField(verbose_name="название", max_length=255)
    is_draft = BooleanField(
        verbose_name="черновик", default=True,
        help_text="задачи в этом статусе недоступны для решения"
    )
    created = DateTimeField(verbose_name='дата создания', auto_now_add=True)
    last_modified = DateTimeField(
        verbose_name="дата последнего изменения",
        auto_now=True
    )
    author = ForeignKey(
        UserModel, verbose_name="автор",
        on_delete=SET_NULL, blank=True, null=True
    )
    source = ForeignKey(
        Source, verbose_name='источник',
        blank=True, null=True
    )
    output_type = CharField(
        verbose_name='чекер', max_length=255,
        choices=Checker.choices, default=Checker.STR
    )
    tags = ManyToManyField(Tag, verbose_name='метки', related_name='tasks', blank=True)
    complexity = CharField(
        verbose_name='сложность', max_length=2,
        choices=Complexity.choices,
        help_text=(
            'Балльная система:\n'
            '1-2 учебная (для закрепления части материала темы)\n'
            '3-4 контрольная (требует знания всей темы)\n'
            '5-6 блочная (требует знания нескольких тем)\n'
            '7-8 итоговая (требует знаний по всему курсу)\n'
            '9-10 повышенной сложности (требует знаний в различных областях)'
        )
    )
    content = HTMLField(
        verbose_name="текст задания",
        default="", blank=True, null=True
    )
    tests = JSONField(verbose_name='автотесты', default=list, blank=True, null=True)

    def __str__(self):
        return self.title


class SolutionExample(Model):

    class Meta:
        verbose_name = "эталонное решение"
        verbose_name_plural = "эталонные решения"

    translator = CharField(
        verbose_name='язык',
        choices=Translator.choices,
        max_length=2
    )
    content = TextField(verbose_name='код рещения', blank=True, null=True)
    task = ForeignKey(Task, related_name='solution_examples')

    def __str__(self):
        return ''
