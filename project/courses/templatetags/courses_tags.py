# -*- coding: utf-8 -*-
from django import template
from itertools import chain
from project.courses.models import TreeItem
from project.executors.models import Code
from project.groups.models import Group
from project.modules.models import Module
register = template.Library()


# @register.inclusion_tag('courses\left_menu.html', takes_context=True)
# def left_menu(context):
#     """ записывает древовидную структуру курсов в переменную data"""
#     object = context['object']
#     items = TreeItem.objects.filter(show=True, parent_id=object.id).order_by("lft")
#     return {'menu': items}

@register.inclusion_tag('courses/breadcrumbs.html', takes_context=True)
def courses_breadcrumbs(context):
    """ Построение хлебных крошек от текущего object до корня стркутуры курсов """
    treeitem = context.get('object', None)
    if treeitem:
        context.update({'breadcrumbs': treeitem.get_ancestors()})
    return context


def add_visible_descendants(result, treeitem):
    """ Рекурсивоное получение видимых потомков и добавление в список result """
    for child in treeitem.get_children().filter(show=True):
        result.append(child)
        add_visible_descendants(result, child)


@register.assignment_tag
def get_visible_descendants(treeitem):
    """ Возвращает список всех видимых потомков """
    result = []
    for child in treeitem.get_children().filter(show=True):
        result.append(child)
        add_visible_descendants(result, child)
    return result


@register.assignment_tag
def get_visible_children(treeitem):
    """ Возвращает всех видимых дочерних элементов """
    return treeitem.get_children().filter(show=True)


def set_navigation_level(level_items, ancestors):
    """ Возвращает список элементов навигации на уровне,
        позвоялет рекурсивно построить дерево навигации по цепочке от курса до элемента """
    navigation = []
    for treeitem in level_items:
        nav_item = {
            "tree_name": treeitem.tree_name,
            "url": treeitem.get_absolute_url(),
        }
        if treeitem in ancestors:
            next_level_items = treeitem.get_children().filter(show=True)
            nav_item["children"] = set_navigation_level(next_level_items, ancestors)
        navigation.append(nav_item)
    return navigation


@register.assignment_tag
def get_navigation(treeitem):
    """ Получить
    [
         {
            tree_name = "Тема"
            url = "/tema/"
            children = [
                {...},
                {...},
            ]
         },
         {...},
         {...},
    ]
    """
    # если элемент или родители скрыты то не выводить навигацию
    if not treeitem.show:
        return []
    ancestors = treeitem.get_ancestors(include_self=True)
    for ancestor in ancestors:
        if not ancestor.show:
            return []

    # собрать treeitem нужные для навигации
    first_level_items = ancestors[0].get_children()
    navigation = set_navigation_level(first_level_items, ancestors)
    return navigation


@register.assignment_tag
def get_courses():
    return TreeItem.objects.filter(show=True, level=0)


@register.assignment_tag
def get_example_obj(id):
    return TreeItem.objects.get(id=id)


@register.assignment_tag
def get_module(group_id, module_id):
    context = {}
    module = Module.objects.get(id=module_id)
    group = Group.objects.get(id=group_id)
    members = group.members.all()
    try:
        context['table'] = group.group_module.get(module_id=module_id).get_solutions_as_table(members)
        context['tasks'] = module.treeitems.all().order_by('lft')
    except:
        pass
    return context