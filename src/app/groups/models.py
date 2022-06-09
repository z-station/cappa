from django.db import models
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
from django.urls import reverse
from app.training.models import Course
from app.accounts.enums import UserRole
from app.groups.enums import (
    GroupStatus,
    GroupMemberRole,
    GroupCourseStatisticAccess
)
from app.groups.querysets import GroupQuerySet

UserModel = get_user_model()


class Group(models.Model):

    class Meta:
        verbose_name = 'учебная группа'
        verbose_name_plural = 'учебные группы'

    is_active = models.BooleanField(
        verbose_name="активная",
        default=True
    )
    title = models.CharField(verbose_name='название', max_length=255)
    year = models.PositiveIntegerField(
        verbose_name='учебный год',
        null=True
    )
    owner = models.ForeignKey(
        UserModel,
        verbose_name='владелец',
        null=True,
        on_delete=models.SET_NULL,
        help_text=(
            'Формальное указание владельца. '
            'Для работы с группой достаточно быть в статусе преподавателя'
        )
    )
    status = models.CharField(
        verbose_name='вступление в группу',
        choices=GroupStatus.CHOICES,
        default=GroupStatus.CLOSED,
        max_length=255
    )
    codeword = models.CharField(
        verbose_name='кодовое слово',
        blank=True,
        null=True,
        max_length=255
    )
    content = HTMLField(
        verbose_name='описание',
        blank=True,
        null=True
    )
    creation_date = models.DateTimeField(
        verbose_name="дата создания",
        auto_now_add=True
    )
    show_date_last_seen = models.BooleanField(
        verbose_name='показывать колонку "Дата последнего входа"'
    )
    show_date_joined = models.BooleanField(
        verbose_name='показывать колонку "Дата регистрации"'
    )
    show_status = models.BooleanField(
        verbose_name='показывать колонку "Статус онлайн"'
    )
    members = models.ManyToManyField(
        UserModel,
        through='GroupMember',
        related_name='training_groups'
    )
    courses = models.ManyToManyField(
        Course,
        through='GroupCourse',
        related_name='training_groups'
    )
    objects = GroupQuerySet.as_manager()

    def __str__(self):
        return self.title

    @property
    def is_open(self):
        return self.status == GroupStatus.OPEN

    @property
    def is_closed(self):
        return self.status == GroupStatus.CLOSED

    @property
    def by_codeword(self):
        return self.status == GroupStatus.BY_CODEWORD

    @property
    def status_name(self):
        return GroupStatus.MAP[self.status]

    @property
    def learners(self):
        return self.members.filter(
            group_members__role=GroupMemberRole.LEARNER,
            is_active=True
        ).order_by_name()

    @property
    def teachers(self):
        return self.members.filter(
            group_members__role=GroupMemberRole.TEACHER,
            role=UserRole.TEACHER,
            is_active=True,
        ).order_by_name()

    def get_absolute_url(self):
        return reverse('groups:group', kwargs={'group_id': self.id})

    def get_breadcrumbs(self):
        return [
            {'title': 'Учебные группы', 'url': reverse('groups:groups')}
        ]


class GroupMember(models.Model):

    class Meta:
        unique_together = ('group', 'user')
        ordering = (
            '-role',
            'user__last_name',
            'user__first_name',
            'user__father_name'
        )

    user = models.ForeignKey(
        UserModel,
        verbose_name='участник',
        related_name='group_members'
    )
    group = models.ForeignKey(
        Group,
        related_name='group_members'
    )
    role = models.CharField(
        verbose_name='роль',
        choices=GroupMemberRole.CHOICES,
        default=GroupMemberRole.LEARNER,
        max_length=50
    )

    def __str__(self):
        return self.user.get_full_name()


class GroupCourse(models.Model):

    class Meta:
        verbose_name = 'учебный курс'
        verbose_name_plural = 'учебные курсы'
        unique_together = ['group', 'course']

    group = models.ForeignKey(Group, related_name='group_courses')
    course = models.ForeignKey(Course, verbose_name='курс')
    statistics_access = models.CharField(
        verbose_name='доступ к групповой статистике',
        help_text='отвечает за видимость таблицы с итогами курса',
        choices=GroupCourseStatisticAccess.CHOICES,
        default=GroupCourseStatisticAccess.ALLOW_FOR_ALL,
        max_length=100
    )

    def __str__(self):
        return self.course.__str__()

    def statistics_allow_for_teacher(self):
        return (
            self.statistics_access in {
                GroupCourseStatisticAccess.ONLY_FOR_TEACHERS,
                GroupCourseStatisticAccess.ALLOW_FOR_ALL,
            }
        )

    def statistics_allow_for_learner(self):
        return (
            self.statistics_access ==
            GroupCourseStatisticAccess.ALLOW_FOR_ALL
        )

    def statistics_is_closed(self):
        return (
            self.statistics_access ==
            GroupCourseStatisticAccess.CLOSED
        )

    def get_breadcrumbs(self):
        return [
            {'title': 'Учебные группы', 'url': reverse('groups:groups')},
            {'title': self.group.title, 'url': reverse('groups:group', kwargs={'group_id': self.group.id})}
        ]
