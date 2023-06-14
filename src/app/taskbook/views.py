from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, Http404, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.translators.enums import TranslatorType
from app.taskbook.forms import TaskBookForm
from app.tasks.models import Solution
from app.tasks.forms import ReviewSolutionForm


@method_decorator(login_required, name='dispatch')
class TaskBookView(View):
    num_tasks = 10  # количество задач на странице

    # TODO taskbook.html фильтр закрывается при клике на какой-либо элемент,
    def get(self, request, *args, **kwargs):
        tasks_list = [{'number': '1', 'name': 'Один',
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
class TaskBookTaskitemView(View):

    def get_object(self) -> Solution:
        # TODO нужно передать тестовую задачу, которая создана через админку
        #  pk = self.kwargs['pk'] использовать для боевого режима
        pk = 1
        if self.request.user.is_teacher:
            return get_object_or_404(Solution, pk=pk)
        else:
            return get_object_or_404(Solution, pk=pk, user=self.request.user)

    def get(self, request, *args, **kwargs):
        solution = [

        ]
        return render(
            request,
            template_name='taskbook/taskitem/template.html',
            context={
                'object': solution,
                'form': [],

                }
            )

    ''' (
        ReviewSolutionForm(instance=solution)
        if request.user.is_teacher else None
    ) '''
