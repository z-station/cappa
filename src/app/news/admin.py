# -*- coding:utf-8 -*-
from django.contrib import admin
from app.news.models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):

    model = News
    list_editable = ('show',)
    list_display = ('title', 'date', 'image', 'show')

