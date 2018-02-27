# -*- coding: utf-8 -*-
from django import template
from project.cms.models import Course
from project.cms.models import Topic
from project.cms.models import Task
register = template.Library()


@register.inclusion_tag('cms\left_menu.html')
def left_menu():
    """ записывает древовидную структуру курсов в переменную data"""
    data = []
    courses = Course.objects.all()
    for course in courses:
        course_data = {
            'title': course.title,
            'url': course.get_absolute_url()
        }
        topics = []
        topics_ids = course.tree.get().get_children().values_list('object_id', flat=True)
        topics2 = Topic.objects.filter(id__in=topics_ids)
        for topic in topics2:
            topic_data = {
                'title': topic.title,
                'url': topic.get_absolute_url()
            }
            tasks = []
            tasks_ids = topic.tree.get().get_children().values_list('object_id', flat=True)
            tasks2 = Task.objects.filter(id__in=tasks_ids)
            for task in tasks2:
                task_data = {
                    'title': task.title,
                    'url': task.get_absolute_url()
                }
                tasks.append(task_data)
            topic_data['tasks'] = tasks
            topics.append(topic_data)
            course_data['topics'] = topics
        data.append(course_data)

    return {'menu': data}

