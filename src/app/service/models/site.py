# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from app.service.enums import SiteAccessType


class SiteSettings(Site):

    class Meta:
        verbose_name = 'настройки сайта'
        verbose_name_plural = verbose_name

    confirm_signup = models.BooleanField(
        verbose_name='требуется подтверждение учетной записи после регистрации',
        default=False
    )
    signup = models.BooleanField(
        verbose_name='регистрация',
        default=True,
        help_text='Регистрация новых пользователей открыта'
    )
    signin = models.CharField(
        verbose_name='Авторизация разрешена',
        choices=SiteAccessType.CHOICES,
        default=SiteAccessType.ALL,
        max_length=255
    )
    logo_title = models.TextField(verbose_name='текст логотипа', blank=True, null=True, default='')
    logo_desc = models.TextField(verbose_name='описание логотипа', blank=True, null=True, default='')
    copyright = models.TextField(
        verbose_name='копирайт', blank=True, null=True, default='',
        help_text='формат: "© <текст копирайта ГГГГ> - текущий год", заполнять только часть в скобках'
    )


__all__ = ('SiteSettings',)
