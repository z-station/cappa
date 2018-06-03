from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.utils import timezone
from collections import OrderedDict
from project.courses.models import TreeItem
from project.executors.models import UserSolution, Code
from project.modules.models import Module


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
    modules = models.ManyToManyField(Module, verbose_name='Модули', blank=True, through='GroupModule')
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

    def get_members(self):
        return self.owners.all() | self.members.all()

    def get_members_number(self):
        return self.owners.count() + self.members.count()

    get_members_number.short_description = 'Участников'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self._state.adding and self.__status != self.status:
            self.changed_status = timezone.now
        super(Group, self).save(force_insert, force_update, using, update_fields)


class GroupModule(models.Model):
    STOCK = 0
    HIDE = 1
    TIMER = 2
    STATES = (
        (STOCK, 'Доступен'),
        (HIDE, 'Скрыт'),
        (TIMER, 'Таймер'),
    )

    module = models.ForeignKey(Module, verbose_name='Модуль')
    group = models.ForeignKey(Group, verbose_name='Группа', related_name='group_module')
    state = models.IntegerField(verbose_name='Статус', choices=STATES, default=STOCK)
    open_at = models.DateTimeField(verbose_name='Открыть', default=timezone.now)
    close_at = models.DateTimeField(verbose_name='Закрыть', default=timezone.now)

    def __str__(self):
        return self.module.name

    def is_active(self):
        """ Если модуль активен возвращает True """
        if (self.state == self.STOCK) or (self.open_at < timezone.now() < self.close_at):
            return True
        return False

    def get_timer(self):
        """  docstring """
        if self.state == self.TIMER:
            now = timezone.now()
            if now < self.open_at:
                return 'Отктроется в %s' % self.format_time(self.open_at)
            elif now > self.close_at:
                return 'Закрылся в %s' % self.format_time(self.close_at)
            else:
                return 'Доступен до %s' % self.format_time(self.close_at)
        return self.STATES[self.state][1]

    @staticmethod
    def format_time(time):
        return time.strftime('%H:%M (%a, %d.%m.%y)')

    def get_solutions_as_table(self):
        """ Возвращает объект (в формате таблицы) с данными о решении задач модуля участниками группы
        table =
            {
                'caption': 'Проверка травами',
                'thead': {
                    -1: {'text': 'Участник/Задача', 'url': ""},
                     0: {'text': 'task1', 'url': '/courses/theme1/task1/'},
                     2: {'text': 'task2', 'url': '/courses/theme1/task2/'}
                },
                'tbody': [
                  {
                   -1: {'text': 'Klava', 'url': ""},
                    0: {'text': '100%', 'url': "", 'class': "success"},
                    2: {'text': ""', 'url': "", 'class': "absent"},
                  },
                  {
                    -1: {'text': 'Karl', 'url': ""),
                     1: {'text': '33%', 'url': "", 'class': "process"},
                     2: {'text': '100%', 'url': "", 'class': "success"},
                  },
              ]
            }
        * где каждая ячейка таблицы содержит след. данные:
          1: {                    # id блока кода (для первого столбика -1)
             'text': '33%',       # текст выводимый в ячейке
             'url': None,         # ссылка ячейки (на стр. задачи, детали решения, профиля польз)
             'class': "process"   # css-класс для стилизации ячейки
             },
        * обратить внимание что treeitem может содержать несколько блоков кода code,
          потому в таблицу попадают блоки кода, а не treeitem
        """

        # элементы дерева привязанные к модулю, у порядоченные как в структуре курсов
        treeitems_ids = self.module.treeitems.all().values_list("id", flat=True).order_by("lft")
        # блоки кода данных элементов дерева (которые сохраняют польз. решения при исполнении)
        codes = Code.objects.filter(treeitem__in=treeitems_ids, save_solutions=True)
        # заполнение ячеек th шапки таблицы thead
        thead = OrderedDict()
        first_th = {
            "text": "Участник/Задача",
            "url": "",
        }
        thead[-1] = first_th
        for code in codes:
            th = {
                "text": code.get_title(),
                "url": code.treeitem.get_absolute_url(),
            }
            thead[code.id] = th

        # заполнение строк tr и их ячеек td тела таблицы tbody
        tbody = []
        # получить решения по данным задачам codes для указанного пользователя user
        for user in self.group.members.all().order_by("last_name", "first_name", "username"):
            tr = OrderedDict()
            first_td = {
                "text": user.get_full_name() if user.get_full_name() else user.username,
                "url": "",  # TODO позже будет ссылка на профиль пользователья
            }
            tr[-1] = first_td
            for code in codes:
                try:
                    user_solution = UserSolution.objects.get(user=user, code=code)
                    css_class = "process"
                    if user_solution.progress == 0:
                        css_class = "unluck"
                    elif user_solution.progress == 100:
                        css_class = "success"

                    text = ""
                    if user_solution.progress != 0:
                        text = str(user_solution.progress) + "%"

                    td = {
                        "text": text,
                        "url": "",  # TODO позже будет ссылка на детали решения
                        "class": css_class
                    }
                except UserSolution.DoesNotExist:
                    td = {
                        "text": "",
                        "url": "",
                        "class": "absent",
                    }
                tr[code.id] = td
            tbody.append(tr)
        caption = self.module.name
        table = {
            "caption": caption,
            "thead": thead,
            "tbody": tbody,
        }
        return table

