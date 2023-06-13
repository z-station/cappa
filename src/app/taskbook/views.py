from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.translators.enums import TranslatorType
from app.taskbook.forms import TaskBookForm


@method_decorator(login_required, name='dispatch')
class TaskBookView(View):
    num_tasks = 10  # количество задач на странице

    def get(self, request, *args, **kwargs):
        tasks_list = [{'number': '1', 'name': 'Один',
                       'difficulty': 'нормально', 'rate': '94', 'solved': True},
                      {'number': '2', 'name': 'Два',
                       'difficulty': 'нормально', 'rate': '94', 'solved': True},
                      {'number': '3', 'name': 'Три',
                       'difficulty': 'нормально', 'rate': '16', 'solved': True},
                      {'number': '4', 'name': 'Четыре',
                       'difficulty': 'нормально', 'rate': '94', 'solved': True},
                      {'number': '5', 'name': 'Пять',
                       'difficulty': 'нормально', 'rate': '74', 'solved': True},
                      {'number': '6', 'name': 'Шесть',
                       'difficulty': 'нормально', 'rate': '94', 'solved': True},
                      {'number': '7', 'name': 'Семь',
                       'difficulty': 'нормально', 'rate': '30', 'solved': True},
                      {'number': '8', 'name': 'Восемь',
                       'difficulty': 'нормально', 'rate': '25', 'solved': True},
                      {'number': '9', 'name': 'Девять',
                       'difficulty': 'нормально', 'rate': '58', 'solved': True},
                      {'number': '10', 'name': 'Десять',
                       'difficulty': 'нормально', 'rate': '61', 'solved': True},
                      {'number': '11', 'name': 'Одиннадцать',
                       'difficulty': 'нормально', 'rate': '7', 'solved': True},
                      {'number': '12', 'name': 'Двенадцать',
                       'difficulty': 'нормально', 'rate': '12', 'solved': True},
                      {'number': '13', 'name': 'Тринадцать',
                       'difficulty': 'нормально', 'rate': '8', 'solved': True},
                      {'number': '14', 'name': 'Четырнадцать',
                       'difficulty': 'нормально', 'rate': '42', 'solved': True},
                      {'number': '15', 'name': 'Пятнадцать',
                       'difficulty': 'нормально', 'rate': '11', 'solved': True},
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
                 'difficulty': 'нормально', 'rate': '94', 'solved': True},
                {'number': '2', 'name': 'Два',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True},
                {'number': '3', 'name': 'Три',
                 'difficulty': 'нормально', 'rate': '16', 'solved': True},
                {'number': '4', 'name': 'Четыре',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True},
                {'number': '5', 'name': 'Пять',
                 'difficulty': 'нормально', 'rate': '74', 'solved': True},
                {'number': '6', 'name': 'Шесть',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True},
                {'number': '7', 'name': 'Семь',
                 'difficulty': 'нормально', 'rate': '30', 'solved': True},
                {'number': '8', 'name': 'Восемь',
                 'difficulty': 'нормально', 'rate': '25', 'solved': True},
                {'number': '9', 'name': 'Девять',
                 'difficulty': 'нормально', 'rate': '58', 'solved': True},
                {'number': '10', 'name': 'Десять',
                 'difficulty': 'нормально', 'rate': '61', 'solved': True},
                {'number': '11', 'name': 'Одиннадцать',
                 'difficulty': 'нормально', 'rate': '7', 'solved': True},
                {'number': '12', 'name': 'Двенадцать',
                 'difficulty': 'нормально', 'rate': '12', 'solved': True},
                {'number': '13', 'name': 'Тринадцать',
                 'difficulty': 'нормально', 'rate': '8', 'solved': True},
                {'number': '14', 'name': 'Четырнадцать',
                 'difficulty': 'нормально', 'rate': '42', 'solved': True},
                {'number': '15', 'name': 'Пятнадцать',
                 'difficulty': 'нормально', 'rate': '11', 'solved': True},
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
                 'difficulty': 'нормально', 'rate': '94', 'solved': True},
                {'number': '2', 'name': 'Два',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True},
                {'number': '3', 'name': 'Три',
                 'difficulty': 'нормально', 'rate': '16', 'solved': True},
                {'number': '4', 'name': 'Четыре',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True},
                {'number': '5', 'name': 'Пять',
                 'difficulty': 'нормально', 'rate': '74', 'solved': True},
                {'number': '6', 'name': 'Шесть',
                 'difficulty': 'нормально', 'rate': '94', 'solved': True},
                {'number': '7', 'name': 'Семь',
                 'difficulty': 'нормально', 'rate': '30', 'solved': True},
                {'number': '8', 'name': 'Восемь',
                 'difficulty': 'нормально', 'rate': '25', 'solved': True},
                {'number': '9', 'name': 'Девять',
                 'difficulty': 'нормально', 'rate': '58', 'solved': True},
                {'number': '10', 'name': 'Десять',
                 'difficulty': 'нормально', 'rate': '61', 'solved': True},
                {'number': '11', 'name': 'Одиннадцать',
                 'difficulty': 'нормально', 'rate': '7', 'solved': True},
                {'number': '12', 'name': 'Двенадцать',
                 'difficulty': 'нормально', 'rate': '12', 'solved': True},
                {'number': '13', 'name': 'Тринадцать',
                 'difficulty': 'нормально', 'rate': '8', 'solved': True},
                {'number': '14', 'name': 'Четырнадцать',
                 'difficulty': 'нормально', 'rate': '42', 'solved': True},
                {'number': '15', 'name': 'Пятнадцать',
                 'difficulty': 'нормально', 'rate': '11', 'solved': True},
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

    def get(self, request, *args, **kwargs):
        return render(request,
                      template_name='taskbook/taskitem/template.html',
                      context={

                      })
