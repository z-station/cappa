from django.db import models
from django.contrib.auth import get_user_model
from src.training.models import Course
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
    _members = models.ManyToManyField(UserModel, through='GroupMember', related_name='training_groups')

    def __str__(self):
        return self.title

    @property
    def members(self):
        return self._members.all().order_by('last_name')

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
    course = models.ForeignKey(Course, verbose_name='курс', limit_choices_to={'show': True})
    show_table = models.BooleanField(verbose_name='отображать таблицу результатов', default=False)

    def __str__(self):
        return self.course.__str__()

    def get_breadcrumbs(self):
        return [
            {'title': 'Учебные группы', 'url': reverse('groups:groups')},
            {'title': self.group.title, 'url': reverse('groups:group', kwargs={'group_id': self.group.id})}
        ]