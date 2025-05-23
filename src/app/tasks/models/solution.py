from django.shortcuts import reverse
from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DateTimeField,
    PositiveIntegerField,
    TextField,
    FloatField,
    BooleanField,
    SET_NULL
)
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
from app.tasks.enums import (
    TaskItemType,
    ReviewStatus,
    ScoreMethod,
)
from app.tasks.models import Task, Source
from app.translators.enums import TranslatorType
from app.tasks.querysets import SolutionQueryset


UserModel = get_user_model()


class Solution(Model):

    class Meta:
        verbose_name = "решение задачи"
        verbose_name_plural = "решения задач"
        ordering = ('-created',)

    type = CharField(
        verbose_name='источник решения',
        choices=TaskItemType.CHOICES,
        max_length=100
    )
    type_id = PositiveIntegerField(
        verbose_name='идентификатор источника решения',
        null=True
    )
    type_name = CharField(
        verbose_name='название источника решения',
        max_length=255,
        null=True
    )
    description = HTMLField(
        verbose_name='описание',
        null=True
    )
    user_first_name = CharField(
        verbose_name='имя',
        max_length=50,
        null=True
    )
    user_last_name = CharField(
        verbose_name='фамилия',
        max_length=50,
        null=True
    )
    user_father_name = CharField(
        verbose_name='отчество',
        max_length=50,
        null=True
    )
    user_email = CharField(
        verbose_name='почта',
        max_length=100,
        null=True
    )
    user_username = CharField(
        verbose_name='логин',
        max_length=200,
        null=True
    )
    user = ForeignKey(
        UserModel,
        verbose_name="пользователь",
        related_name='solutions',
        on_delete=SET_NULL,
        null=True
    )
    task_name = CharField(
        verbose_name='название задачи',
        max_length=500
    )
    task = ForeignKey(
        Task,
        verbose_name="задача",
        related_name='solutions',
        on_delete=SET_NULL,
        null=True
    )
    created = DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True
    )
    score_method = CharField(
        verbose_name='метод оценивания',
        max_length=50,
        choices=ScoreMethod.CHOICES,
        default=ScoreMethod.TESTS
    )
    testing_score = FloatField(
        verbose_name='оценка',
        null=True
    )
    count_tests = PositiveIntegerField(
        verbose_name='кол-во тестов',
        null=True
    )
    count_passed_tests = PositiveIntegerField(
        verbose_name='кол-во пройденных тестов',
        null=True
    )
    content = TextField(
        verbose_name="листинг решения"
    )
    translator = CharField(
        verbose_name="язык",
        choices=TranslatorType.CHOICES,
        max_length=100
    )
    review_score = FloatField(
        verbose_name='оценка',
        null=True
    )
    review_status = CharField(
        verbose_name='статус',
        max_length=255,
        choices=ReviewStatus.CHOICES,
        null=True,
    )
    reviewer = ForeignKey(
        UserModel,
        verbose_name='преподаватель',
        on_delete=SET_NULL,
        null=True,
        related_name='reviewed_solutions',
        help_text=(
            'заполняется автоматически, когда преподаватель выставляет оценку'
        )
    )
    reviewer_first_name = CharField(
        verbose_name='имя преподавателя',
        max_length=50,
        null=True
    )
    reviewer_last_name = CharField(
        verbose_name='фамилия преподавателя',
        max_length=50,
        null=True
    )
    reviewer_father_name = CharField(
        verbose_name='отчество преподавателя',
        max_length=50,
        null=True
    )
    reviewer_comment = HTMLField(
        verbose_name="комментарий преподавателя",
        blank=True,
        null=True
    )
    review_date = DateTimeField(
        verbose_name="дата проверки",
        null=True
    )
    due_date = DateTimeField(
        verbose_name="срок сдачи",
        null=True
    )
    hide_review_score = BooleanField(
        verbose_name="скрыть оценку",
        default=False
    )
    hide_reviewer_comment = BooleanField(
        verbose_name="скрыть комментарий",
        default=False
    )
    max_score = PositiveIntegerField(
        verbose_name='максимальный балл за решение',
        null=True,
    )
    external_source = ForeignKey(
        Source,
        verbose_name='внешний источник решения',
        on_delete=SET_NULL,
        null=True,
        related_name='solutions'
    )
    external_source_name = CharField(
        verbose_name='источник решения',
        default='сайт',
        max_length=100,
        null=True
    )
    rating_is_calculated = BooleanField(
        verbose_name='решение учтено в рейтинге',
        default=False
    )
    score = FloatField(
        verbose_name='итоговая оценка',
        null=True,
        help_text='рассчитывается автоматически'
    )
    objects = SolutionQueryset.as_manager()

    @property
    def review_status_name(self) -> str:
        return ReviewStatus.MAP[self.review_status]

    @property
    def review_status_awaiting_check(self) -> bool:
        return (
            self.score_method in ScoreMethod.REVIEW_METHODS
            and self.review_status in ReviewStatus.AWAITING_CHECK
        )

    @property
    def translator_name(self):
        return TranslatorType.MAP.get(self.translator, '-')

    @property
    def type_name_value(self):
        return TaskItemType.MAP[self.type]

    @property
    def score_method_name(self):
        return ScoreMethod.MAP[self.score_method]

    # TODO в зависимости от типа проверки использовать для рейтинга разные значения

    @property
    def score_method_is_tests(self):
        return self.score_method == ScoreMethod.TESTS

    @property
    def score_method_is_review(self):
        return self.score_method == ScoreMethod.REVIEW

    @property
    def score_method_is_tests_and_review(self):
        return self.score_method == ScoreMethod.TESTS_AND_REVIEW

    @property
    def is_internal(self):
        return self.type != TaskItemType.EXTERNAL

    @property
    def is_external(self):
        return self.type == TaskItemType.EXTERNAL

    @property
    def type_course(self):
        return self.type == TaskItemType.COURSE

    @property
    def reviewer_full_name(self):
        if self.reviewer_first_name:
            return (
                f'{self.reviewer_last_name} '
                f'{self.reviewer_first_name} '
                f'{self.reviewer_father_name or ""}'
            )
        else:
            return ''

    @property
    def user_full_name(self):
        if self.user_first_name:
            return (
                f'{self.user_last_name} '
                f'{self.user_first_name} '
                f'{self.user_father_name or ""}'
            )
        else:
            return ''

    def get_absolute_url(self):
        return reverse('solutions:solution', kwargs={'pk': self.id})

    def get_breadcrumbs(self):
        return [
            {
                'title': 'Список решений',
                'url': f'{reverse("solutions:solutions")}?task_id={self.task_id}'
            },
        ]

    def __str__(self):
        return (
            f'{self.user_last_name} {self.user_first_name}: {self.task_name}'
        )

    def __repr__(self):
        return self.__str__()


class ExternalSolution(Solution):

    class Meta:
        proxy = True
        verbose_name = "внешнее решение"
        verbose_name_plural = "внешние решения"
        ordering = ('-created',)

    def __str__(self):
        return (
            f'{self.external_source_name}: {self.task_name}'
        )

    def __repr__(self):
        return self.__str__()
