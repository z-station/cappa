# -*- coding:utf-8 -*-
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, Http404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from src.training.models import TaskItem, Solution, Course
from src.training.forms import TaskItemForm
from src.groups.models import GroupCourse


UserModel = get_user_model()


class TaskItemView(View):

    def get_object(self, request, *args, **kwargs):
        try:
            return TaskItem.objects \
                .select_related('task', 'topic__course', 'topic__course__lang') \
                .get(slug=kwargs['taskitem'], topic__slug=kwargs['topic'], topic__course__slug=kwargs['course'])
        except TaskItem.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        taskitem = self.get_object(request,  *args, **kwargs)
        solution = None
        form_initial = {'lang': taskitem.lang.provider}
        if request.user.is_active:
            solution = Solution.objects.filter(taskitem=taskitem, user=request.user).first()
            if solution:
                form_initial['content'] = solution.last_changes
        form = TaskItemForm(initial=form_initial)
        return render(
            request=request,
            template_name='training/taskitem/template.html',
            context={
                'course': taskitem.topic.course,
                'object': taskitem,
                'solution': solution,
                'form': form
            }
        )

    def post(self, request, *args, **kwargs):
        taskitem = self.get_object(request, *args, **kwargs)
        form = TaskItemForm(data=request.POST)
        response = form.perform_operation(request.user, taskitem)
        return JsonResponse(response.__dict__)


class SolutionView(View):

    def get_object(self, request, *args, **kwargs):

        try:
            user_id = request.GET.get('user')
            if user_id and int(user_id) == request.user.id:
                # Запрос решения участника сделан самим участником группы
                return Solution.objects.get(
                    taskitem__slug=kwargs['taskitem'],
                    taskitem__topic__slug=kwargs['topic'],
                    taskitem__topic__course__slug=kwargs['course'],
                    user_id=user_id
                )
            elif user_id:
                # Запрос решения участника сделан владельцем группы
                user = UserModel.objects.get(id=user_id)
                group = user.member.filter(group__author=request.user).first().group
                group_course = GroupCourse.objects.filter(course__slug=kwargs['course'], group=group)
                if group_course.exists():
                    return Solution.objects.get(
                        taskitem__slug=kwargs['taskitem'],
                        taskitem__topic__slug=kwargs['topic'],
                        taskitem__topic__course__slug=kwargs['course'],
                        user=user
                    )
                else:
                    raise Http404
            else:
                # Запрос собственного решения
                return Solution.objects.get(
                    taskitem__slug=kwargs['taskitem'],
                    taskitem__topic__slug=kwargs['topic'],
                    taskitem__topic__course__slug=kwargs['course'],
                    user_id=request.user.id
                )

        except (ObjectDoesNotExist, ValueError, AttributeError):
            raise Http404

    def get(self, request, *args, **kwargs):
        solution = self.get_object(request, *args, **kwargs)
        return render(
            request,
            template_name='training/solution.html',
            context={
                'object': solution,
                'course': solution.taskitem.topic.course
            }
        )


@method_decorator(login_required, name='dispatch')
class CourseSolutionsView(View):

    def get(self, request, *args, **kwargs):
        try:
            course = Course.objects.get(slug=kwargs.get('course'))
            user_id = request.GET['user_id']
            user = UserModel.objects.get(id=user_id, is_active=True)
            return JsonResponse(user.get_cache_course_solutions_data(course))
        except:
            raise Http404
