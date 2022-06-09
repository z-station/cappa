# -*- coding:utf-8 -*-
from django.contrib.auth import get_user_model
from django.shortcuts import render, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from app.training.models import TaskItem
from app.tasks.models import Draft, Solution


UserModel = get_user_model()


class TaskItemView(View):

    def get_object(self, request, *args, **kwargs):
        try:
            return TaskItem.objects.select_related(
                'task',
                'topic__course'
            ).get(
                show=True,
                slug=kwargs['taskitem'],
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
            template_name='training/taskitem/template.html',
            context={
                'course': taskitem.topic.course,
                'object': taskitem,
                'solutions_exists': solutions_exists
            }
        )
