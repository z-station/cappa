from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
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

    def paginate_result(self, qst: QuerySet) -> QuerySet:
        paginator = Paginator(qst, 30)  # Show 30 contacts per page
        page = self.request.GET.get('page', 1)
        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            result = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            result = paginator.page(paginator.num_pages)
        return result

    def get(self, request, *args, **kwargs):
        taskitems = self.queryset
        if 'clear' in request.GET:
            taskbook_filter = TaskBookFilter()
        else:
            taskbook_filter = TaskBookFilter(
                data=request.GET,
                queryset=self.queryset
            )
            if taskbook_filter.is_valid():
                taskitems = taskbook_filter.qs
        taskitems = self.paginate_result(taskitems)
        return render(
            request=request,
            template_name='taskbook/taskbook.html',
            context={
              'taskitems': taskitems,
              'form': taskbook_filter.form,
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
