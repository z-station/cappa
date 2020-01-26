# -*- coding: utf-8 -*-
from django import template
from src.news.models import News
register = template.Library()


@register.assignment_tag
def get_news():
    return News.objects.filter(show=True)
