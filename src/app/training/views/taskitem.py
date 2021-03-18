# -*- coding:utf-8 -*-
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, Http404
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from app.training.models import TaskItem, Solution, Course
from app.training.forms import TaskItemForm, SolutionForm
from app.translators.consts import translators_external_urls
from app.translators.entities.response import OperationResponse

UserModel = get_user_model()


@method_decorator(login_required, name='dispatch')
class TaskItemView(View):

    def get_object(self, request, *args, **kwargs):
        try:
            return TaskItem.objects \
                .select_related('task', 'topic__course') \
                .get(slug=kwargs['taskitem'], topic__slug=kwargs['topic'], topic__course__slug=kwargs['course'])
        except TaskItem.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        taskitem = self.get_object(request,  *args, **kwargs)
        solution = None
        form_initial = {'translator': taskitem.translator}
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
                'form': form,
                'translators_urls': translators_external_urls
            }
        )

    def post(self, request, *args, **kwargs):
        taskitem = self.get_object(request, *args, **kwargs)
        form = TaskItemForm(data=request.POST)
        response: OperationResponse = form.perform_operation(request.user, taskitem)
        return JsonResponse(response)


@method_decorator(login_required, name='dispatch')
class SolutionView(View):

    PERM_DENIED = 0
    VIEW_PERM = 1
    CHANGE_PERM = 2

    def get_solution_user_id(self, request) -> int:

        """ Возвращает id пользователя, чье решение запрашивается

        Возможно 3 варианта:
            - в get-параметра 'user' указан id целевого пользователя
            - get-параметр не указан, тогда возвращает id текущего пользователя
            - get-параметр не целое число, тога возбуждаем 404 ошибку
        """

        target_user_id = request.GET.get('user')
        if target_user_id is None:
            solution_user_id = int(request.user.id)
        elif target_user_id.isdigit():
            solution_user_id = int(target_user_id)
        else:
            raise Http404
        return solution_user_id

    def get_user_perm(self, request, solution_user_id: int) -> int:

        """
        Возвращает права пользователя на запрашиваемое решение:

            Доступ к просмотру решения имеют 3 группы пользователей:
            1. Суперпользователь
            2. Автор решения
            3. Автор группы (учитель) в которой состоит пользователь (ученик)

            Доступ к редактированию решения имеют 2 группы пользователей:
            1. Суперпользователь
            2. Автор группы (учитель) в которой состоит пользователь (ученик)

        """
        if request.user.is_superuser:
            perm = self.CHANGE_PERM
        else:
            solution_user = UserModel.objects.filter(id=solution_user_id).first()
            if solution_user.member.filter(group__author=request.user).exists():  # преподаватель в группе ученика
                perm = self.CHANGE_PERM
            elif solution_user_id == request.user.id:  # просмотр собственного решения
                perm = self.VIEW_PERM
            else:
                perm = self.PERM_DENIED
        return perm

    def get_object(self, user_id, **kwargs) -> Solution:
        filter = {
            "taskitem__slug": kwargs['taskitem'],
            "taskitem__topic__slug": kwargs['topic'],
            "taskitem__topic__course__slug": kwargs['course'],
            "user_id": user_id
        }
        try:
            return Solution.objects.get(**filter)
        except MultipleObjectsReturned:
            # TODO Логировать ошибку
            return Solution.objects.filter(**filter).first()
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        solution_user_id = self.get_solution_user_id(request)
        solution = self.get_object(user_id=solution_user_id, **kwargs)
        request_user_perm = self.get_user_perm(request, solution_user_id)
        form = None
        if request_user_perm == self.CHANGE_PERM and solution.taskitem.manual_check:
            form = SolutionForm(instance=solution)
        elif request_user_perm == self.PERM_DENIED:
            raise Http404

        return render(
            request,
            template_name='training/solution/template.html',
            context={
                'object': solution,
                'form': form,
                'course': solution.taskitem.topic.course,
                'topic': solution.taskitem.topic
            }
        )

    def post(self, request, *args, **kwargs):
        solution_user_id = self.get_solution_user_id(request)
        solution = self.get_object(user_id=solution_user_id, **kwargs)
        request_user_perm = self.get_user_perm(request, solution_user_id)
        if request_user_perm == self.CHANGE_PERM and solution.taskitem.manual_check:
            form = SolutionForm(instance=solution, data=request.POST)
            if form.is_valid():
                solution = form.save(commit=False)
                solution.teacher = request.user
                solution.save()
        else:
            raise Http404
        return render(
            request,
            template_name='training/solution/template.html',
            context={
                'object': solution,
                'form': form,
                'course': solution.taskitem.topic.course,
                'topic': solution.taskitem.topic
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
