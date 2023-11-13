from django.db import models
from django.contrib.auth import get_user_model
from filebrowser.fields import FileBrowseField


UserModel = get_user_model()


class Database(models.Model):

    class Meta:
        verbose_name = 'пользовательская база данных'
        verbose_name_plural = 'пользовательские базы данных'

    name = models.CharField(
        verbose_name='название',
        max_length=255,
    )
    created = models.DateTimeField(
        verbose_name='дата создания',
        auto_now=True
    )
    last_changes = models.DateTimeField(
        verbose_name='дата изменения',
        auto_now_add=True
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
        null=True
    )
    file = FileBrowseField(
        verbose_name='файл',
        max_length=1000,
        extensions=['.sql',],
        blank=True,
        null=True,
        help_text='Файл данных PostgreSQL версии не ниже 13'
    )
    author = models.ForeignKey(
        UserModel,
        verbose_name='владелец'
    )

    @property
    def db_name(self):
        return f'db_{self.id}'

    def __str__(self):
        return self.name
