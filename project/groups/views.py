# -*- coding:utf-8 -*-
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from project.groups.models import Group


class GroupsView(generic.ListView):
    template_name = 'groups/groups.html'
    context_object_name = 'groups'
    paginate_by = 20

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            return Group.objects.filter(Q(name__icontains=search))
        return Group.objects.all()


class MyGroupsView(generic.ListView):
    template_name = 'groups/my_groups.html'
    context_object_name = 'groups'
    paginate_by = 20

    def get_queryset(self):
        search = self.request.GET.get('search')
        my_groups = self.request.user.ownership.all()\
            .union(self.request.user.membership.all())
        if search:
            return my_groups.filter(Q(name__icontains=search))
        return my_groups


class GroupView(generic.DetailView):
    model = Group
    template_name = 'groups/group.html'

    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)

        context['position'] = context['group'].get_user_position(self.request.user)
        if context['position'] >= Group.OWNER:
            context['members'] = context['group'].members.all()

        context['modules_data'] = context['group'].group_module.all()

        return context


# TODO Переделать. 1. Создать и согласовать json-структуру таблицы. 2 GroupModule лишнее звено - сохранять в кэш
class GroupProgressView(generic.DetailView):
    model = Group
    template_name = 'groups/progress.html'

    def get_context_data(self, **kwargs):
        context = super(GroupProgressView, self).get_context_data(**kwargs)

        get_object_or_404(context['group'].owners, pk=self.request.user.pk)

        context['tables'] = []
        members = context['group'].members.all()
        for group_module in context['group'].group_module.all():
            table_data = group_module.get_solutions_as_table(members)
            context['tables'].append(table_data)

        return context


def join(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    if group.members.filter(pk=request.user.pk):
        group.members.remove(request.user)
        messages.info(request, 'Вы больше не участник группы "{}".'.format(group.name))
        return HttpResponseRedirect(reverse('groups:my_groups'))
    elif group.owners.filter(pk=request.user.pk):
        if group.owners.all()[0].pk != request.user.pk:
            group.owners.remove(request.user)
            messages.info(request, 'Вы больше не владелец группы "{}".'.format(group.name))
            return HttpResponseRedirect(reverse('groups:my_groups'))
    elif group.state != group.CLOSE:
        if group.state == group.CODE and request.POST['codeword'] != group.codeword:
            messages.error(request, 'Неверное кодовое слово!')
            return HttpResponseRedirect(reverse('groups:group', args=(group.pk, )))
        group.members.add(request.user)
        messages.info(request, 'Вы вступили в группу "{}".'.format(group.name))

    return HttpResponseRedirect(reverse('groups:group', args=(group.pk, )))
