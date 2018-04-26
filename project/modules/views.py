from django.views import generic

from project.modules.models import Module


class ModulesView(generic.ListView):
    template_name = 'modules/modules.html'
    context_object_name = 'modules'
    paginate_by = 10

    def get_queryset(self):
        return Module.objects.all().order_by('id')


class ModuleView(generic.DetailView):
    model = Module
    template_name = 'modules/module.html'
