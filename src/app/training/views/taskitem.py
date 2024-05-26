# -*- coding:utf-8 -*-
from django.contrib.auth import get_user_model
from django.shortcuts import render, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from app.tasks.models import Solution, TaskItem
from app.tasks.enums import TaskItemType
from app.translators.enums import TranslatorType


UserModel = get_user_model()


@method_decorator(login_required, name='dispatch')
class TaskItemView(View):

    def get_object(self, request, *args, **kwargs):
        try:
            return TaskItem.objects.select_related(
                'task',
                'topic__course'
            ).get(
                show=True,
                type=TaskItemType.COURSE,
                slug=kwargs['taskitem'],
                topic__show=True,
                topic__slug=kwargs['topic'],
                topic__course__slug=kwargs['course']
            )
        except TaskItem.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        taskitem = self.get_object(request,  *args, **kwargs)
        solutions_exists = Solution.objects.internal().by_user(
            request.user.id
        ).by_task(
            taskitem.task_id
        ).exists()
        return render(
            request=request,
            template_name='training/taskitem.html',
            context={
                'course': taskitem.topic.course,
                'object': taskitem,
                'solutions_exists': solutions_exists,
                'translator': taskitem.translator[0],
                'sql_translator': (
                    taskitem.translator[0] == TranslatorType.POSTGRESQL
                )
            }
        )
