from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, Http404
from django.utils.decorators import method_decorator
from django.views.generic import View
from app.taskbook.filters import TaskBookFilter
from app.tasks.models import Solution, TaskItem
from app.tasks.enums import TaskItemType
from app.translators.enums import TranslatorType

UserModel = get_user_model()


@method_decorator(login_required, name='dispatch')
class TaskBookView(View):

    num_tasks = 10  # количество задач на странице
    queryset = TaskItem.objects.show().type_taskbook()

    # TODO taskbook.html фильтр закрывается при клике на какой-либо элемент,
    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.queryset, self.num_tasks)
        page = request.GET.get('page')
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)
        return render(
            request=request,
            template_name='taskbook/taskbook.html',
            context={
              'page': page,
              'tasks': tasks,
              'filter': TaskBookFilter(),
            }
        )

    def post(self, request, *args, **kwargs):
        taskitem_filter = TaskBookFilter(
            data=request.POST,
            queryset=self.queryset
        )
        tasks_list = taskitem_filter.qs
        paginator = Paginator(tasks_list, self.num_tasks)
        page = request.GET.get('page')
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)
        return render(
            request,
            template_name='taskbook/taskbook.html',
            context={
              'page': page,
              'tasks': tasks,
              'filter': taskitem_filter,
            }
        )


@method_decorator(login_required, name='dispatch')
class TaskItemView(View):

    def get_object(self, request, *args, **kwargs):
        try:
            return TaskItem.objects.select_related(
                'task'
            ).get(
                show=True,
                type=TaskItemType.TASKBOOK,
                slug=kwargs['taskitem'],
            )
        except TaskItem.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        taskitem = self.get_object(request, *args, **kwargs)
        solutions_exists = Solution.objects.by_user(
            request.user.id
        ).internal().by_task(
            taskitem.task_id
        ).exists()
        return render(
            request=request,
            template_name='taskbook/taskitem.html',
            context={
                'object': taskitem,
                'solutions_exists': solutions_exists,
                'translator': taskitem.translator[0],
                'sql_translator': (
                    taskitem.translator[0] == TranslatorType.POSTGRESQL
                )
            }
        )
