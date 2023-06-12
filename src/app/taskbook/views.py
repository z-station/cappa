from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import HttpResponseNotFound

from app.translators.enums import TranslatorType
from app.taskbook.forms import TaskBookForm


@method_decorator(login_required, name='dispatch')
class TaskBookView(View):

    def get(self, request, *args, **kwargs):
        return render(request,
                      template_name='taskbook/taskbook.html',
                      context={
                          'tasks': [{'number': '1', 'name': 'задача1',
                                     'difficulty': 'нормально', 'rate': '94', 'solved': True},
                                    {'number': '2', 'name': 'задача1',
                                     'difficulty': 'нормально', 'rate': '94', 'solved': True},
                                    {'number': '3', 'name': 'задача1',
                                     'difficulty': 'нормально', 'rate': '94', 'solved': True}],
                          # TODO спросить как настроить для каждого поля формы свой input
                          #  (особенно для MultipleChoiseField)
                          'form': TaskBookForm(),
                      })

    def post(self, request, *args, **kwargs):
        form = TaskBookForm(data=request.POST)
        if form.is_valid():
            return render(request,
                          template_name='taskbook/taskbook.html',
                          context={
                              'tasks': [{'number': '1', 'name': 'З1', 'difficulty': 'нормально', 'rate': '94',
                                         'solved': True},
                                        {'number': '2', 'name': 'З2', 'difficulty': 'нормально', 'rate': '94',
                                         'solved': True},
                                        {'number': '3', 'name': 'З3', 'difficulty': 'нормально', 'rate': '94',
                                         'solved': True}],
                              'form': form,
                          })
        else:
            return render(request,
                          template_name='taskbook/taskbook.html',
                          context={
                              'tasks': [{'number': '1', 'name': 'З1', 'difficulty': 'нормально', 'rate': '94',
                                         'solved': True},
                                        {'number': '2', 'name': 'З2', 'difficulty': 'нормально', 'rate': '94',
                                         'solved': True},
                                        {'number': '3', 'name': 'З3', 'difficulty': 'нормально', 'rate': '94',
                                         'solved': True}],
                              'form': form,
                          })


@method_decorator(login_required, name='dispatch')
class TaskBookTaskitemView(View):

    def get(self, request, *args, **kwargs):
        return render(request,
                      template_name='taskbook/taskitem/template.html',
                      context={

                      })
