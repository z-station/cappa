from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, Http404, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.translators.enums import TranslatorType
from app.taskbook.forms import TaskBookForm
from app.tasks.models import Solution
from app.training.models import TaskItem
from app.tasks.forms import ReviewSolutionForm

UserModel = get_user_model()


@method_decorator(login_required, name='dispatch')
class TaskBookView(View):
    num_tasks = 10  # количество задач на странице

    # TODO taskbook.html фильтр закрывается при клике на какой-либо элемент,
    def get(self, request, *args, **kwargs):
        tasks_list = [
            {'number': '1', 'name': 'Один',
             'difficulty': 'нормально', 'rate': '94', 'solved': True,
             'url': "/taskitem"},
            {'number': '2', 'name': 'Два',
             'difficulty': 'нормально', 'rate': '94', 'solved': True,
             'url': "/taskitem"},
            {'number': '3', 'name': 'Три',
             'difficulty': 'нормально', 'rate': '16', 'solved': True,
             'url': "/taskitem"},
            {'number': '4', 'name': 'Четыре',
             'difficulty': 'нормально', 'rate': '94', 'solved': True,
             'url': "/taskitem"},
            {'number': '5', 'name': 'Пять',
             'difficulty': 'нормально', 'rate': '74', 'solved': True,
             'url': "/taskitem"},
            {'number': '6', 'name': 'Шесть',
             'difficulty': 'нормально', 'rate': '94', 'solved': True,
             'url': "/taskitem"},
            {'number': '7', 'name': 'Семь',
             'difficulty': 'нормально', 'rate': '30', 'solved': True,
             'url': "/taskitem"},
            {'number': '8', 'name': 'Восемь',
             'difficulty': 'нормально', 'rate': '25', 'solved': True,
             'url': "/taskitem"},
            {'number': '9', 'name': 'Девять',
             'difficulty': 'нормально', 'rate': '58', 'solved': True,
             'url': "/taskitem"},
            {'number': '10', 'name': 'Десять',
             'difficulty': 'нормально', 'rate': '61', 'solved': True,
             'url': "/taskitem"},
            {'number': '11', 'name': 'Одиннадцать',
             'difficulty': 'нормально', 'rate': '7', 'solved': True,
             'url': "/taskitem"},
            {'number': '12', 'name': 'Двенадцать',
             'difficulty': 'нормально', 'rate': '12', 'solved': True,
             'url': "/taskitem"},
            {'number': '13', 'name': 'Тринадцать',
             'difficulty': 'нормально', 'rate': '8', 'solved': True,
             'url': "/taskitem"},
            {'number': '14', 'name': 'Четырнадцать',
             'difficulty': 'нормально', 'rate': '42', 'solved': True,
             'url': "/taskitem"},
            {'number': '15', 'name': 'Пятнадцать',
             'difficulty': 'нормально', 'rate': '11', 'solved': True,
             'url': "/taskitem"},
        ]
        paginator = Paginator(tasks_list, self.num_tasks)
        page = request.GET.get('page')
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)
        return render(request,
                      template_name='taskbook/taskbook.html',
                      context={
                          'page': page,
                          'tasks': tasks,
                          # TODO спросить как настроить для каждого поля формы свой input
                          #  (особенно для MultipleChoiseField)
                          'form': TaskBookForm(),
                      })

    def post(self, request, *args, **kwargs):
        form = TaskBookForm(data=request.POST)
        if form.is_valid():
            # TODO тут будет фильтрация по форме фильтра
            #  и в контекст будут передаваться только задачи, проходящие фильтры
            tasks_list = [
                {'number': '1', 'name': 'Один',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True,
                 'url': "/taskitem"},
                {'number': '2', 'name': 'Два',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True,
                 'url': "/taskitem"},
                {'number': '3', 'name': 'Три',
                 'difficulty': 'нормально', 'rate': '16', 'solved': True,
                 'url': "/taskitem"},
                {'number': '4', 'name': 'Четыре',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True,
                 'url': "/taskitem"},
                {'number': '5', 'name': 'Пять',
                 'difficulty': 'нормально', 'rate': '74', 'solved': True,
                 'url': "/taskitem"},
                {'number': '6', 'name': 'Шесть',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True,
                 'url': "/taskitem"},
                {'number': '7', 'name': 'Семь',
                 'difficulty': 'нормально', 'rate': '30', 'solved': True,
                 'url': "/taskitem"},
                {'number': '8', 'name': 'Восемь',
                 'difficulty': 'нормально', 'rate': '25', 'solved': True,
                 'url': "/taskitem"},
                {'number': '9', 'name': 'Девять',
                 'difficulty': 'нормально', 'rate': '58', 'solved': True,
                 'url': "/taskitem"},
                {'number': '10', 'name': 'Десять',
                 'difficulty': 'нормально', 'rate': '61', 'solved': True,
                 'url': "/taskitem"},
                {'number': '11', 'name': 'Одиннадцать',
                 'difficulty': 'нормально', 'rate': '7', 'solved': True,
                 'url': "/taskitem"},
                {'number': '12', 'name': 'Двенадцать',
                 'difficulty': 'нормально', 'rate': '12', 'solved': True,
                 'url': "/taskitem"},
                {'number': '13', 'name': 'Тринадцать',
                 'difficulty': 'нормально', 'rate': '8', 'solved': True,
                 'url': "/taskitem"},
                {'number': '14', 'name': 'Четырнадцать',
                 'difficulty': 'нормально', 'rate': '42', 'solved': True,
                 'url': "/taskitem"},
                {'number': '15', 'name': 'Пятнадцать',
                 'difficulty': 'нормально', 'rate': '11', 'solved': True,
                 'url': "/taskitem"},
            ]
            paginator = Paginator(tasks_list, self.num_tasks)
            page = request.GET.get('page')
            try:
                tasks = paginator.page(page)
            except PageNotAnInteger:
                tasks = paginator.page(1)
            except EmptyPage:
                tasks = paginator.page(paginator.num_pages)
            return render(request,
                          template_name='taskbook/taskbook.html',
                          context={
                              'page': page,
                              'tasks': tasks,
                              # TODO спросить как настроить для каждого поля формы свой input
                              #  (особенно для MultipleChoiseField)
                              'form': TaskBookForm(),
                          })
        else:
            tasks_list = [
                {'number': '1', 'name': 'Один',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True,
                 'url': "/taskitem"},
                {'number': '2', 'name': 'Два',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True,
                 'url': "/taskitem"},
                {'number': '3', 'name': 'Три',
                 'difficulty': 'нормально', 'rate': '16', 'solved': True,
                 'url': "/taskitem"},
                {'number': '4', 'name': 'Четыре',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True,
                 'url': "/taskitem"},
                {'number': '5', 'name': 'Пять',
                 'difficulty': 'нормально', 'rate': '74', 'solved': True,
                 'url': "/taskitem"},
                {'number': '6', 'name': 'Шесть',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True,
                 'url': "/taskitem"},
                {'number': '7', 'name': 'Семь',
                 'difficulty': 'нормально', 'rate': '30', 'solved': True,
                 'url': "/taskitem"},
                {'number': '8', 'name': 'Восемь',
                 'difficulty': 'нормально', 'rate': '25', 'solved': True,
                 'url': "/taskitem"},
                {'number': '9', 'name': 'Девять',
                 'difficulty': 'нормально', 'rate': '58', 'solved': True,
                 'url': "/taskitem"},
                {'number': '10', 'name': 'Десять',
                 'difficulty': 'нормально', 'rate': '61', 'solved': True,
                 'url': "/taskitem"},
                {'number': '11', 'name': 'Одиннадцать',
                 'difficulty': 'нормально', 'rate': '7', 'solved': True,
                 'url': "/taskitem"},
                {'number': '12', 'name': 'Двенадцать',
                 'difficulty': 'нормально', 'rate': '12', 'solved': True,
                 'url': "/taskitem"},
                {'number': '13', 'name': 'Тринадцать',
                 'difficulty': 'нормально', 'rate': '8', 'solved': True,
                 'url': "/taskitem"},
                {'number': '14', 'name': 'Четырнадцать',
                 'difficulty': 'нормально', 'rate': '42', 'solved': True,
                 'url': "/taskitem"},
                {'number': '15', 'name': 'Пятнадцать',
                 'difficulty': 'нормально', 'rate': '11', 'solved': True,
                 'url': "/taskitem"},
            ]
            paginator = Paginator(tasks_list, self.num_tasks)
            page = request.GET.get('page')
            try:
                tasks = paginator.page(page)
            except PageNotAnInteger:
                tasks = paginator.page(1)
            except EmptyPage:
                tasks = paginator.page(paginator.num_pages)
            return render(request,
                          template_name='taskbook/taskbook.html',
                          context={
                              'page': page,
                              'tasks': tasks,
                              'form': TaskBookForm(),
                          })


@method_decorator(login_required, name='dispatch')
class TaskItemView(View):

    def get_object(self, request, *args, **kwargs):
        try:
            return TaskItem.objects.select_related(
                'task'
                # 'topic__course'
            ).get(
                show=True,
                # slug=kwargs['taskitem'],
                # topic__slug=kwargs['topic'],
                # topic__course__slug=kwargs['course']
            )
        except TaskItem.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        taskitem = self.get_object(request, *args, **kwargs)
        solutions_exists = Solution.objects.internal().by_user(
            request.user.id
        ).by_task(
            taskitem.task_id
        ).exists()
        if taskitem.translator == TranslatorType.POSTGRESQL:
            template = 'taskbook/taskitem/sql_template.html'
        else:
            template = 'taskbook/taskitem/template.html'
        return render(
            request=request,
            template_name=template,
            context={
                # 'course': taskitem.topic.course,
                'object': taskitem,
                'solutions_exists': solutions_exists
            }
        )
