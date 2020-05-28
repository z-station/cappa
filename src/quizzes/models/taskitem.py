import json
from django.core.cache import cache
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from tinymce.models import HTMLField
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from src.tasks.models import Task
from src.quizzes.models import Quiz
from src.utils.fields import OrderField, SlugField
from src.utils.consts import langs


UserModel = get_user_model()


class TaskItem(models.Model):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ['order_key']

    show = models.BooleanField(verbose_name="отображать", default=True)
    task = models.ForeignKey(Task, verbose_name='задача', related_name='quizzes')
    max_score = models.PositiveIntegerField(verbose_name='балл за решение', default=5)
    manual_check = models.BooleanField(verbose_name='ручная проверка', default=False)
    compiler_check = models.BooleanField(verbose_name='проверка автотестами', default=True)
    slug = SlugField(verbose_name="слаг", max_length=255, blank=True, null=True, for_fields=['quiz'])
    langg = models.CharField(
        verbose_name='язык', choices=langs.CHOICES,
        blank=True, null=True, max_length=255
    )
    
    number = models.PositiveIntegerField(verbose_name='порядковый номер', blank=True, null=True)
    order_key = OrderField(verbose_name='порядок', blank=True, null=True, for_fields=['quiz'])
    quiz = models.ForeignKey(Quiz, verbose_name='самостоятельная работа', related_name='_taskitems')

    @property
    def lang(self):
        return self.quiz.lang

    @property
    def title(self):
        return self.task.title

    @property
    def numbered_title(self):
        data = self.get_cache_data()
        return '%s %s' % (data['number'], data['title'])

    @property
    def cache_key(self):
        return 'taskitem__%d' % self.id

    def get_data(self):
        return {
            'id': self.cache_key,
            'number': '%s.' % (self.number),
            'title': self.title,
            'url': reverse('quizzes:taskitem', kwargs={
                    'quiz': self.quiz.slug,
                    'taskitem': self.slug
                }
            )
        }


    def get_cache_data(self):
        json_data = cache.get(self.cache_key)
        if not json_data:
            data = self.get_data()
            cache.set(self.cache_key, json.dumps(data, ensure_ascii=False))
        else:
            data = json.loads(json_data)
        return data

    def get_breadcrumbs(self):
        return [
            {'title': 'Самостоятельные работы', 'url': reverse('quizzes:quizzes')},
            {'title': self.quiz.title,   'url': self.quiz.get_absolute_url()},
        ]

    def get_absolute_url(self):
        return self.get_cache_data()['url']

    def __str__(self):
        return self.title


class Solution(models.Model):

    class Meta:
        verbose_name = "решение задачи"
        verbose_name_plural = "решения задач"

    MS__NOT_CHECKED = '0'
    MS__READY_TO_CHECK = '1'
    MS__CHECK_IN_PROGRESS = '2'
    MS__CHECKED = '3'
    MS__AWAITING_CHECK = (MS__READY_TO_CHECK, MS__CHECK_IN_PROGRESS)
    MS__CHOICES = (
        (MS__NOT_CHECKED, 'нет'),
        (MS__READY_TO_CHECK, 'ожидает проверки'),
        (MS__CHECK_IN_PROGRESS, 'в процессе проверки'),
        (MS__CHECKED, 'проверено'),
    )

    S__NONE = '0'
    S__UNLUCK = '1'
    S__IN_PROGRESS = '2'
    S__SUCCESS = '3'
    S__CHOICES = (
        (S__NONE, 'нет попыток'),
        (S__UNLUCK, 'нет решения'),
        (S__IN_PROGRESS, 'частично решено'),
        (S__SUCCESS, 'решено'),
    )

    taskitem = models.ForeignKey(TaskItem, verbose_name='задача', related_name='solutions')
    user = models.ForeignKey(UserModel, verbose_name="пользователь", related_name='_solution_quizzes')
    datetime = models.DateTimeField(verbose_name='дата/время отправки', blank=True, null=True)
    is_count = models.BooleanField(verbose_name="баллы идут в зачет", default=True)
    is_locked = models.BooleanField(verbose_name="запрещено изменять", default=False)
    manual_status = models.CharField(
        verbose_name='статус проверки преподавателем', max_length=255,
        choices=MS__CHOICES, default=MS__NOT_CHECKED
    )
    manual_score = models.FloatField(verbose_name='оценка преподавателя', blank=True, null=True)
    tests_score = models.FloatField(verbose_name='оценка по автотестам', blank=True, null=True)

    last_changes = models.TextField(verbose_name="последние изменения", blank=True, default='')
    content = models.TextField(verbose_name="листинг решения", blank=True, default='')
    version_list = JSONField(verbose_name="список сохраненных решений", default=list, blank=True, null=True)
    comment = HTMLField(verbose_name="комментарий к решению", blank=True, null=True)
    teacher = models.ForeignKey(
        UserModel, verbose_name='преподаватель', blank=True, null=True, related_name='controlled_solutions_quizzes',
        help_text='заполняется автоматически, когда преподаватель выставляет оценку'
    )


    @property
    def score(self):

        """ Оценка преподавателя имеет больший приоритет чем оценка по автотестам """

        if self.taskitem.manual_check:
            if self.manual_status == self.MS__CHECKED:
                return self.manual_score
            else:
                return None
        else:
            return self.tests_score

    @property
    def status(self) -> str:

        """ Статус вычисляется на основе оценки """

        if self.score is None:
            return self.S__NONE
        elif self.score <= 0:
            return self.S__UNLUCK
        elif self.score >= self.taskitem.max_score:
            return self.S__SUCCESS
        else:
            return self.S__IN_PROGRESS

    @property
    def status_name(self) -> str:
        
        """ Возващает текст статуса """
        
        status = self.status
        for choice in self.S__CHOICES:
            if choice[0] == status:
                return choice[1]

    @property
    def manual_status_name(self):
        for choice in self.MS__CHOICES:
            if choice[0] == self.manual_status:
                return choice[1]

    def create_version(self, content):

        """ Создать верисю решения задачи """

        if len(self.version_list) == 10:
            self.version_list.pop(0)
        self.version_list.append({
            "datetime": str(timezone.now().strftime(format='%Y-%m-%d %H:%M:%S.%f')),
            "content": content,
        })

    def set_is_count(self):

        """ Если время на решение задачи истекло, то решение вне зачета """

        if self.taskitem.quiz.end_time is not None:
            self.is_count = timezone.now() <= self.taskitem.quiz.end_time

    def get_breadcrumbs(self):
        return [
            {'title': 'Самостоятельные работы', 'url': reverse('quizzes:quizzes')},
            {'title': self.taskitem.quiz.title,   'url': self.taskitem.quiz.get_absolute_url()},
        ]

    def get_absolute_url(self):
        return reverse(
            'quizzes:solution',
            kwargs={
                'quiz': self.taskitem.quiz.slug,
                'taskitem': self.taskitem.slug
            }
        )

    def __str__(self):
        return '%s: %s' % (self.user.get_full_name(), self.taskitem.title)

    def __repr__(self):
        return f"Solution: {self.__str__()}"


__all__ = ['TaskItem', 'Solution']
