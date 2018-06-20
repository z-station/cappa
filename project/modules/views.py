from django.shortcuts import get_object_or_404
from django.views import generic

from project.groups.models import Group
from project.modules.models import Module


class ModulesView(generic.ListView):
    template_name = 'modules/modules.html'
    context_object_name = 'modules'
    paginate_by = 10

    def get_queryset(self):
        return Module.objects.all()


class MyModulesView(generic.ListView):
    template_name = 'modules/modules.html'
    context_object_name = 'modules'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MyModulesView, self).get_context_data(**kwargs)
        context['my_modules'] = True

        return context

    def get_queryset(self):
        return self.request.user.modules.all()


class ModuleProgressView(generic.DetailView):
    model = Module
    template_name = 'modules/module.html'

    def get_context_data(self, **kwargs):
        context = super(ModuleProgressView, self).get_context_data(**kwargs)

        group_id = self.kwargs.pop('group_id', None)
        if group_id:
            context['group'] = get_object_or_404(Group, pk=group_id, modules=context['module'])
            context['position'] = context['group'].get_user_position(self.request.user)
            if context['position']:
                if context['position'] == Group.OWNER:
                    members = context['group'].members.all()
                else:
                    members = context['group'].members.filter(pk=self.request.user.pk)
                    print(members)

                context['table'] = context['group'].group_module.get(module_id=context['module'].id)\
                    .get_solutions_as_table(members)

        if context['module'].owner.pk == self.request.user.pk:
            context['my_module'] = True

        context['tasks'] = context['module'].treeitems.all()

        return context
