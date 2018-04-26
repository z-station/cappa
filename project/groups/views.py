from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from project.groups.models import Group


class GroupsView(generic.ListView):
    template_name = 'groups/groups.html'
    context_object_name = 'groups'
    paginate_by = 10

    def get_queryset(self):
        return Group.objects.all().order_by('id')


class GroupView(generic.DetailView):
    model = Group
    template_name = 'groups/group.html'

    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            try:
                if context['group'].members.get(pk=self.request.user.pk):
                    context['member'] = True
            except self.request.user.DoesNotExist:
                context['member'] = False
        return context


def join(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.user.is_authenticated():
        if request.method == 'POST':
            try:
                if group.members.get(pk=request.user.pk):
                    group.members.remove(request.user)
            except request.user.DoesNotExist:
                if group.state != 0:
                    if group.state != 2:
                        group.members.add(request.user)
                    elif request.POST['codeword'] == group.codeword:
                        group.members.add(request.user)
    else:
        return HttpResponseRedirect(reverse('groups:groups'))

    return HttpResponseRedirect(reverse('groups:group', args=(group.pk,)))
