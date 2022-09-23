from typing import Optional
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField
)
from app.accounts.enums import UserRole
from app.accounts.managers import CustomUserManager


class User(AbstractUser):

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    username = CharField(
        verbose_name='логин',
        max_length=150,
        unique=True,
        help_text=(
            'Обязательно. 150 не более символов. '
            'Буквы, цифры и знаки @/./+/-/_ only.'
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': "Пользователь с таким логином уже существует.",
        },
    )

    father_name = CharField(
        verbose_name='отчество',
        max_length=30,
        blank=True
    )

    role = CharField(
        verbose_name='роль',
        choices=UserRole.CHOICES,
        default=UserRole.LEARNER,
        max_length=20,
        help_text='Преподаватели имеют доступ ко всем решениям'
    )

    objects = CustomUserManager()

    @property
    def is_teacher(self):
        return self.role == UserRole.TEACHER

    @property
    def last_seen_time(self) -> Optional[int]:
        from app.accounts.services import UserService
        return UserService.get_last_seen(self)

    @property
    def is_online(self) -> bool:
        from app.accounts.services import UserService
        return UserService.user_is_online(self)

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.father_name}'

    def get_short_full_name(self):
        first_name = f'{self.first_name[0].upper()}.' if self.first_name else ''
        father_name = f'{self.father_name[0].upper()}.' if self.father_name else ''
        return f'{self.last_name} {first_name} {father_name}'

    def __str__(self):
        return self.get_full_name()
