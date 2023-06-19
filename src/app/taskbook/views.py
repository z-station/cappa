from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, Http404
from django.utils.decorators import method_decorator
from django.views.generic import View

from app.taskbook.forms import TaskBookForm
from app.taskbook.filters import TaskBookFilter
from app.tasks.models import Solution
from app.taskbook.models import TaskBookItem
from app.translators.enums import TranslatorType

UserModel = get_user_model()


@method_decorator(login_required, name='dispatch')
class TaskBookView(View):

    num_tasks = 10  # количество задач на странице

    def get_queryset(self, request, *args, **kwargs):
        # TODO изучить querysets
        return TaskBookItem.objects.filter(show=True)

    # TODO taskbook.html фильтр закрывается при клике на какой-либо элемент,
    def get(self, request, *args, **kwargs):
        tasks_list = self.get_queryset(request, *args, **kwargs)
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
                          'filter': TaskBookFilter(),
                      })

    def post(self, request, *args, **kwargs):
        taskitem_filter = TaskBookFilter(request.POST, queryset=TaskBookItem.objects.filter(show=True))
        tasks_list = taskitem_filter.qs
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
                          'filter': taskitem_filter,
                      })


@method_decorator(login_required, name='dispatch')
class TaskItemView(View):

    def get_object(self, request, *args, **kwargs):
        try:
            return TaskBookItem.objects.select_related(
                'task'
            ).get(show=True, slug=kwargs['taskitem'])
        except TaskBookItem.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        taskitem = self.get_object(request, *args, **kwargs)
        solutions_exists = Solution.objects.by_user(
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
                'object': taskitem,
                'solutions_exists': solutions_exists
            }
        )
