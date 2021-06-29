from typing import List, Dict
from django.db import models
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from app.training.models import Course
from tinymce.models import HTMLField
from django.urls import reverse

UserModel = get_user_model()


class Group(models.Model):

    class Meta:
        verbose_name = 'учебная группа'
        verbose_name_plural = 'учебные группы'

    OPEN = '0'
    CLOSE = '1'
    CODE = '2'
    CHOICES = (
        (OPEN, 'открыто'),
        (CLOSE, 'закрыто'),
        (CODE, 'по кодовому слову'),
    )

    show = models.BooleanField(verbose_name="отображать", default=True)
    title = models.CharField(verbose_name='название', max_length=255)
    author = models.ForeignKey(UserModel, verbose_name='автор')
    status = models.CharField(verbose_name='вступление в группу', choices=CHOICES, default=CLOSE, max_length=255)
    codeword = models.CharField(verbose_name='кодовое слово', blank=True, null=True, max_length=255)
    content = HTMLField(verbose_name='описание', blank=True, null=True)
    creation_date = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    show_date_last_seen = models.BooleanField(verbose_name='показывать колонку "Дата последнего входа"')
    show_date_joined = models.BooleanField(verbose_name='показывать колонку "Дата регистрации"')
    show_status = models.BooleanField(verbose_name='показывать колонку "Статус"')
    _members = models.ManyToManyField(UserModel, through='GroupMember', related_name='training_groups')

    def __str__(self):
        return self.title

    @property
    def members(self):
        return self._members.filter(
            is_active=True
        ).order_by('last_name')

    def get_members_data(self) -> List[Dict]:
        result = []
        users__last_seen = cache.get('users__last_seen') or {}
        datetime_now = timezone.now().timestamp()
        for user in self.members:
            user_cached_data = users__last_seen.get(user.id)
            if user_cached_data is None:
                last_seen = user.last_login.timestamp()
            else:
                last_seen = int(user_cached_data['last_seen'])
            is_online = (last_seen + settings.USER_ONLINE_TIMEOUT) >= datetime_now
            result.append({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'last_seen': last_seen,
                'date_joined': user.date_joined,
                'is_online': is_online
            })
        return result

    def get_status(self):
        for choice in self.CHOICES:
            if self.status == choice[0]:
                return choice[1]

    def get_absolute_url(self):
        return reverse('groups:group', kwargs={'group_id': self.id})

    def get_breadcrumbs(self):
        return [
            {'title': 'Учебные группы', 'url': reverse('groups:groups')}
        ]


class GroupMember(models.Model):

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'
        unique_together = ['group', 'user']
        ordering = ['user__last_name']

    user = models.ForeignKey(UserModel, verbose_name='участник', related_name='member')
    group = models.ForeignKey(Group, related_name='member')

    def __str__(self):
        return self.user.get_full_name()


class GroupCourse(models.Model):

    class Meta:
        verbose_name = 'учебный курс'
        verbose_name_plural = 'учебные курсы'
        unique_together = ['group', 'course']

    group = models.ForeignKey(Group, related_name='group_courses')
    course = models.ForeignKey(Course, verbose_name='курс')
    show_table = models.BooleanField(verbose_name='отображать таблицу результатов', default=False)

    def __str__(self):
        return self.course.__str__()

    def get_breadcrumbs(self):
        return [
            {'title': 'Учебные группы', 'url': reverse('groups:groups')},
            {'title': self.group.title, 'url': reverse('groups:group', kwargs={'group_id': self.group.id})}
        ]