from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from app.translators.enums import TranslatorType


@method_decorator(login_required, name='dispatch')
class TaskbookView(View):

    def get(self, request, *args, **kwargs):
        return render(request,
                      template_name='taskbook/taskbook.html',
                      context={

                      })

    def post(self, request, *args, **kwargs):
        pass


@method_decorator(login_required, name='dispatch')
class TaskbookTaskitemView(View):

    def get(self, request, *args, **kwargs):
        return render(request,
                      template_name='taskbook/taskitem/template.html',
                      context={

                      })
