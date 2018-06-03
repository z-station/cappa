# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.template import RequestContext

from project.groups.models import Group


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

            context['modules_data'] = context['group'].group_module.all()

        return context


# TODO Переделать. 1. Создать и согласовать json-структуру таблицы. 2 GroupModule лишнее звено - сохранять в кэш
def progress(request, group_id):

    """ Добавление доп. переменных в шаблон """
    group = get_object_or_404(Group, id=group_id)
    user_is_owner = group.owners.filter(id=request.user.id)
    if not user_is_owner:
        return HttpResponseRedirect(reverse('groups:groups'))

    tables = []
    for group_module in group.group_module.all():
        table_data = group_module.get_solutions_as_table()
        tables.append(table_data)

    template = "groups/progress.html"
    context = {"tables": tables, "object": group}
    return render(request, template, context)


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
