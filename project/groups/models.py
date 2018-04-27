from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from project.modules.models import Module
from project.modules.fields import JSONField


class Group(models.Model):
    OPEN = 0
    CLOSE = 1
    CODE = 2
    STATE = (
        (OPEN, 'Открытая'),
        (CLOSE, 'Закрытая'),
        (CODE, 'Кодовое слово'),
    )
    OWNER = 100
    MEMBER = 101

    name = models.CharField(max_length=64, help_text='Введите название группы', verbose_name='Название')
    status = models.TextField(help_text='Введите статус группы', verbose_name='Статус', blank=True)
    changed_status = models.DateTimeField(default=timezone.now)
    owners = models.ManyToManyField(User, verbose_name='Владельцы', related_name='ownership')
    members = models.ManyToManyField(User, verbose_name='Пользователи', related_name='membership', blank=True)
    modules = models.ManyToManyField(Module, verbose_name='Модули', blank=True, through='ModuleData')
    progress = JSONField(blank=True, null=True)
    state = models.IntegerField(verbose_name='Статус', choices=STATE, default=CLOSE)
    codeword = models.CharField(max_length=64, help_text='Введите кодовое слово', verbose_name='Код', blank=True)
    created_at = models.DateTimeField(verbose_name='Создана', auto_now_add=True)

    class Meta:
        verbose_name = 'Группу'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super(Group, cls).from_db(db, field_names, values)
        instance.__status = values[field_names.index('status')]
        return instance

    def get_state(self):
        return self.STATE[self.state][1]

    def get_root_owner_username(self):
        try:
            return self.owners.all()[0].username
        except IndexError:
            return 'None'

    get_root_owner_username.short_description = 'Владелец'

    def get_owners_usernames(self):
        return ' ,'.join([owner.username for owner in self.owners.all()])

    def get_members_number(self):
        return self.owners.count() + self.members.count()

    get_members_number.short_description = 'Участников'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self._state.adding and self.__status != self.status:
            self.changed_status = timezone.now
        super(Group, self).save(force_insert, force_update, using, update_fields)


class ModuleData(models.Model):
    STOCK = 0
    HIDE = 1
    TIMER = 2
    STATE = (
        (STOCK, 'Доступен'),
        (HIDE, 'Скрыт'),
        (TIMER, 'Таймер'),
    )

    module = models.ForeignKey(Module, verbose_name='Модуль')
    group = models.ForeignKey(Group, verbose_name='Группа', related_name='data')
    state = models.IntegerField(verbose_name='Статус', choices=STATE, default=STOCK)
    open_at = models.DateTimeField(verbose_name='Открыть', default=timezone.now)
    close_at = models.DateTimeField(verbose_name='Закрыть', default=timezone.now)

    def __str__(self):
        return self.module.name

    def get_stock(self):
        if self.state == self.STOCK or self.open_at < timezone.now() < self.close_at:
            return True
        return False

    def get_timer(self):
        if self.state == self.TIMER:
            now = timezone.now()
            if now < self.open_at:
                return 'Отктроется в {0}'.format(self.format_time(self.open_at))
            elif now > self.close_at:
                return 'Закрылся в {0}'.format(self.format_time(self.close_at))
            else:
                return 'Доступен до {0}'.format(self.format_time(self.close_at))
        return self.STATE[self.state][1]

    @staticmethod
    def format_time(time):
        return time.strftime('%H:%M (%a, %d.%m.%y)')
