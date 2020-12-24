# -*- coding: utf-8 -*-
from django.contrib import admin
from app.service.models import Menu, MenuItem
from adminsortable2.admin import SortableInlineAdminMixin


class MenuItemInline(SortableInlineAdminMixin, admin.TabularInline):

    model = MenuItem
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):

    model = Menu
    inlines = (MenuItemInline,)

