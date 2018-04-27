from django.views import generic

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
        context['my'] = True

        return context

    def get_queryset(self):
        return self.request.user.modules.all()


class ModuleView(generic.DetailView):
    model = Module
    template_name = 'modules/module.html'

    def get_context_data(self, **kwargs):
        context = super(ModuleView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            if context['module'].owner.pk == self.request.user.pk:
                context['my'] = True

        context['tasks'] = context['module'].tasks.all()

        return context
