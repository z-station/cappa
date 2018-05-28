# -*- coding: utf-8 -*-
from django import template
from project.courses.models import TreeItem
register = template.Library()


# @register.inclusion_tag('courses\left_menu.html', takes_context=True)
# def left_menu(context):
#     """ записывает древовидную структуру курсов в переменную data"""
#     object = context['object']
#     items = TreeItem.objects.filter(show=True, parent_id=object.id).order_by("lft")
#     return {'menu': items}
