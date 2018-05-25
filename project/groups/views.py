from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from project.executors.models import CodeSolution
from project.groups.models import Group, ModuleData


class GroupsView(generic.ListView):
    template_name = 'groups/groups.html'
    context_object_name = 'groups'
    paginate_by = 10

    def get_queryset(self):
        return Group.objects.all()


class MyGroupsView(generic.ListView):
    template_name = 'groups/groups.html'
    context_object_name = 'groups'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MyGroupsView, self).get_context_data(**kwargs)
        context['ownership'] = self.request.user.ownership.all()
        context['my'] = True

        return context

    def get_queryset(self):
        return self.request.user.membership.all()


class GroupView(generic.DetailView):
    model = Group
    template_name = 'groups/group.html'

    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)

        context['error_message'] = self.request.session.get('error_message', None)
        if context['error_message']:
            del self.request.session['error_message']

        if self.request.user.is_authenticated():
            try:
                if context['group'].members.get(pk=self.request.user.pk):
                    context['position'] = Group.MEMBER
            except self.request.user.DoesNotExist:
                try:
                    if context['group'].owners.get(pk=self.request.user.pk):
                        context['position'] = Group.OWNER
                except self.request.user.DoesNotExist:
                    pass

            context['modules_data'] = context['group'].data.all()

        return context


class ProgressView(generic.DetailView):
    model = Group
    template_name = 'groups/progress.html'

    def get_context_data(self, **kwargs):
        context = super(ProgressView, self).get_context_data(**kwargs)

        try:
            if context['group'].members.get(pk=self.request.user.pk):
                context['position'] = Group.MEMBER
        except self.request.user.DoesNotExist:
            try:
                if context['group'].owners.get(pk=self.request.user.pk):
                    context['position'] = Group.OWNER
            except self.request.user.DoesNotExist:
                # messages.error(self.request, 'Вы не состоите в группе {}'.format(context['group'].name))
                return HttpResponseRedirect(reverse('groups:groups'))

        """
        progress_v2.3a = {
            'tasks': {
                task1.pk: task1.title,
                task2.pk: task2.title,
            },
            user1.pk: {
                'name': user1.username
                task1.pk: [solution1.pk, success],
                task2.pk: [solution2.pk, success],
            },
            user2.pk: {
            },
        }
        """
        context['data'] = []
        for data in context['group'].data.all():
            context['data'].append([])
            tasks = data.progress.pop('tasks', {}).values()
            context['data'][-1].append([data.module.name, ])
            context['data'][-1][-1].extend(tasks)
            for user_pk, row in data.progress.items():
                context['data'][-1].append([row.pop('name'), ])
                for task_pk, cell in row.items():
                    if cell[1]:
                        context['data'][-1][-1].append(True)
                    else:
                        try:
                            solution = CodeSolution.objects.get(code__pk=task_pk, user__pk=user_pk)
                            if solution.success:
                                data_save = ModuleData.objects.get(pk=data.pk)
                                data_save.progress[str(user_pk)][str(task_pk)] = [solution.pk, solution.success]
                                data_save.save()
                                context['data'][-1][-1].append(True)
                            else:
                                context['data'][-1][-1].append(False)
                        except ObjectDoesNotExist:
                            context['data'][-1][-1].append(None)

        return context


def join(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        try:
            if group.members.get(pk=request.user.pk):
                group.members.remove(request.user)
                return HttpResponseRedirect(reverse('groups:my_groups'))
        except request.user.DoesNotExist:
            if group.state != group.CLOSE:
                if group.state == group.CODE:
                    if request.POST['codeword'] != group.codeword:
                        request.session['error_message'] = 'Wrong codeword!'
                        return HttpResponseRedirect(reverse('groups:group', args=(group.pk, )))
                group.members.add(request.user)
    else:
        return HttpResponseRedirect(reverse('groups:groups'))

    return HttpResponseRedirect(reverse('groups:group', args=(group.pk, )))
