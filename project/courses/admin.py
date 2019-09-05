# -*- coding: utf-8 -*-

from django.contrib.admin.utils import label_for_field
from django.contrib import admin
from django.template.response import TemplateResponse
from django.conf.urls import url
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import PermissionDenied
from django.apps import apps
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django import forms
from project.courses.models import TreeItem, TreeItemFlat
from project.courses.grid import GridRow
from project.executors.nested_inline.admin import NestedModelAdmin
from project.executors.models import CodeTest, Code


class LazyEncoder(DjangoJSONEncoder):
    """
    Encoder for lazy translation objects
    Кодирует данные из QuerySet в строку utf-8  для пердачи по сети в формате json
    """
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


class TreeItemAdmin(NestedModelAdmin):
    """ Класс ModelAdmin – это отображение модели в интерфейсе администратора """

    change_list_template = 'admin/courses/tree_list.html'
    model = TreeItem
    list_display = ("title", "author", "show")
    exclude = ("author",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = []
    fieldsets = (
        (
          None, {
              "fields": ("type",("show", "in_number_list"),  "title", "slug", "long_title"),
          }
        ),
        (
            'Короткое описание', {
                "fields": ("about", ),
                "classes": ("collapse", )
            }
        ),
        (
          None, {
              "fields": ("content",),
          }
        ),
    )

    def changelist_view(self, request):

        """Представление Django для страницы отображения всех объектов модели."""
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        opts = self.model._meta
        app_label = opts.app_label
        title = opts.verbose_name
        app_config = apps.get_app_config(app_label)

        context = {
            'app_label': app_label,
            'title': title,
            'opts': opts,
            'app_config': app_config,
            'site_header': self.admin_site.site_header,
            'root_title': "Структура курсов",
        }
        return TemplateResponse(request, self.change_list_template, context)

    def get_node_data(self, treeitem):
        """
        :param treeitem: TreeItem object
        :return: JSON data of TreeItem object and his content_object
        """
        node = {}
        if treeitem.parent is None:
            node['parent'] = '#'
        else:
            node['parent'] = treeitem.parent.id
        if treeitem.leaf is True:
            node['type'] = 'leaf'
        node['id'] = treeitem.id
        node['text'] = treeitem.__str__()
        node['data'] = {}
        change_link = reverse('admin:courses_treeitem_change', args=(treeitem.id,))

        watch_link = reverse('courses-item', args=(treeitem.get_complete_slug(),))
        node['data']['change_link'] = change_link
        node['data']['watch_link'] = watch_link

        if treeitem.leaf is False:
            node['data']['add_links'] = []
            node['data']['add_links'].append(
                {
                   'url': reverse('admin:courses_treeitem_add') + '?target=%s' % treeitem.id,
                   'label': 'Добавить элемент'
                }
            )
        return node

    def json_tree(self, request):
        """
        :param request:
        :return: JSON structure of courses for jsTree
        возвращает все элементы дерева в формате json (в строке)
        """
        tree = []
        if request.user.is_superuser:
            for treeitem in TreeItem.objects.all():
                # объекты принадлежащие текущему пользователю
                tree.append(self.get_node_data(treeitem))
        else:
             for treeitem in TreeItem.objects.filter(author=request.user):
            # объекты принадлежащие текущему пользователю
                tree.append(self.get_node_data(treeitem))

        return JsonResponse(tree, safe=False, encoder=LazyEncoder)

    def move_tree_item(self, request):
        """
        Moves node relative to a given target node as specified
        by position
        :param request:
            request.POST contains item_id, target_id, position
            item_id: id of movable node
            target_id: id of target node
            valid values for position are first-child, last-child, left, right
        :return: JSON data with results of operation
        получаем объект и информацию о  позиции (left/right), куда хотим переместить_id, текущий _id
        если поля не корректно переданы- появится ошибка
        иначе вызов функции node.move_to и перемещение элемента на нужную позицию

        """
        if request.method == "POST":
            position = request.POST.get('position', None)
            target_id = request.POST.get('target_id', None)
            item_id = request.POST.get('item_id', None)

            if item_id and position and target_id:
                try:
                    node = TreeItem.objects.get(id=item_id)
                    target = TreeItem.objects.get(id=target_id)
                except TreeItem.DoesNotExist:
                    message = 'Элемент курса не найден'
                    return JsonResponse({'status': 'error', 'type_message': 'error', 'message': message}, encoder=LazyEncoder)

                if node.slug and not TreeItem.check_slug(target, position, node.slug, node=node):
                    message = 'Передвижение невозможно, ' \
                              'на данном уровне есть элемент с таким-же слагом: "%s"' % node.slug
                    return JsonResponse({'status': 'error', 'type_message': 'error', 'message': message}, encoder=LazyEncoder)

                node.move_to(target, position)
                message = 'Успешное перемещение'
                return JsonResponse({'status': 'OK', 'type_message': 'info',
                                     'message': message}, encoder=LazyEncoder)
        message = 'Метод запроса не POST'
        return JsonResponse({'status': 'error', 'type_message': 'error',
                             'message': message}, encoder=LazyEncoder)

    def delete_tree_item(self, request):
        """
        Delete TreeItem object
        :param request:
            request.POST contains item_id: if of removed TreeItem object
        :return: JSON data with results of operation
        """
        if request.method == "POST":
            item_id = request.POST.get('item_id', None)
            try:
                treeitem = TreeItem.objects.get(id=item_id)
                treeitem.delete()
                message = 'Элемент курса удален'
                return JsonResponse({'status': 'OK', 'type_message': 'info',
                                     'message': message}, encoder=LazyEncoder)
            except TreeItem.DoesNotExist:
                message = 'Элемент курса не существует'
                return JsonResponse({'status': 'error',
                                     'type_message': 'error',
                                     'message': message}, encoder=LazyEncoder)
        message = 'Метод запроса не POST'
        return JsonResponse({'status': 'error', 'type_message': 'error',
                             'message': message}, encoder=LazyEncoder)

    def list_children(self, request, parent_id=None):
        """
        :param parent_id: id of parent TreeItem object
        :return: JSON data with fields for display and list children of
        the parent node
        """

        if parent_id is None:
            if request.user.is_superuser:
                nodes_qs = TreeItem.objects.root_nodes()
            else:
                nodes_qs = TreeItem.objects.root_nodes().filter(author=request.user)

        else:
            if request.user.is_superuser:
                nodes_qs = TreeItem.objects.get(id=int(parent_id)).get_children()
            else:
                nodes_qs = TreeItem.objects.get(id=int(parent_id)).get_children().filter(author=request.user)


        response = {}
        if nodes_qs.count() == 0:
            return JsonResponse(response)

        fields = []
        for field_name in self.list_display:
            if field_name == '__str__':
                field_label = 'Элемент курса'
                fields.insert(0, [field_name, field_label])
            else:
                field_label = label_for_field(field_name, TreeItem, self.__class__)
                fields.append([field_name, field_label])

        nodes = []
        for item in nodes_qs:
            node = GridRow(item, self.list_display, self)
            nodes.append(node.json_data())

        response['fields'] = fields
        response['nodes'] = nodes
        return JsonResponse(response, safe=False, encoder=LazyEncoder)

    def get_form(self, request, obj=None, **kwargs):
        """ Метод возвращает класс формы, переопределим метод валидации слага
            при создании нового элемента курса, проверяя наличие такого слага на данном уровне дерева"""
        # TODO не самое изящное решение, переделать

        FormClass = super(TreeItemAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormCatalogWrapper(FormClass):

            def clean_slug(self):
                slug = self.cleaned_data['slug']
                if obj is None:
                    node = None
                    target = None
                    position = 'last-child'
                else:
                    node = obj
                    target = node
                    position = 'left'
                target_id = request.GET.get('target', None)
                copy_id = request.GET.get('copy', None)
                if target_id or copy_id:
                    try:
                        if target_id:
                            target = TreeItem.objects.get(pk=target_id)
                        elif copy_id:
                            target = TreeItem.objects.get(pk=copy_id).parent
                    except TreeItem.DoesNotExist:
                        pass
                    position = 'last-child'
                if not TreeItem.check_slug(target, position, slug, node):
                    message = 'На данном уровне есть элемент с таким-же слагом: "%s"' % self.cleaned_data['slug']
                    raise forms.ValidationError(message)
                return slug

        return ModelFormCatalogWrapper

    def save_model(self, request, obj, form, change):
        """
        Override save_model.
        Moves TreeItem object if request.POST contains target node or
        copied node
        """
        obj.author = request.user
        target_id = request.GET.get('target', None)
        copy_id = request.GET.get('copy', None)
        target = None
        if target_id or copy_id:
            try:
                if target_id:
                    target = TreeItem.objects.get(pk=target_id)
                elif copy_id:
                    target = TreeItem.objects.get(pk=copy_id)
            except TreeItem.DoesNotExist:
                pass
        obj.save()
        if target and target_id:
            obj.move_to(target, 'last-child')
        if target and copy_id:
            obj.move_to(target.parent, 'last-child')

    def get_urls(self):
        return [
            url(r'^tree/$', self.admin_site.admin_view(self.json_tree)),
            url(r'^move/$', self.admin_site.admin_view(self.move_tree_item)),
            url(r'^delete/$', self.admin_site.admin_view(self.delete_tree_item)),
            url(r'^list_children/(\d+)$', self.admin_site.admin_view(self.list_children)),
            url(r'^list_children/', self.admin_site.admin_view(self.list_children)),
            ] + super(TreeItemAdmin, self).get_urls()


admin.site.register(TreeItem, TreeItemAdmin)


class TreeItemFlatAdmin(NestedModelAdmin):

    def tests(self, obj):
        code = Code.objects.filter(treeitem=obj)
        if code.exists():
            len_tests = CodeTest.objects.filter(code=code[0]).count()
            return len_tests
        return 0

    tests.short_description = "Тесты"

    model = TreeItemFlat
    search_fields = ("title", "author", "source__name", "source_raw_id")
    list_filter = ("author", "type", "source",)
    list_display = ("title", "author", "show", "type", "in_number_list",  "tests", "source", "source_raw_id", )
    search_fields = ("title", "author__username", "source__name", "source_raw_id")
    prepopulated_fields = {"slug": ("title",), }
    raw_id_fields = ("author",)

    fieldsets = (
        (
          None, {
              "fields": (("show", "type"),  "title", "slug", "long_title", ("source_raw_id", "source"), "author"),
          }
        ),
        (
            'Короткое описание', {
                "fields": ("about", ),
                "classes": ("collapse", )
            }
        ),
        (
          None, {
              "fields": ("content",),
          }
        ),
    )

    def get_queryset(self, request):
        """ В списке показывать только те что принадлежат пользователю (супер видет все элементы) """
        qs = super(TreeItemFlatAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author=request.user)

    # def save_model(self, request, obj, form, change):
    #     """
    #     Override save_model.
    #     Moves TreeItem object if request.POST contains target node or
    #     copied node
    #     """
        # if not obj.id and obj.author is None:
        #     obj.author = request.user
        # obj.save()
        # tmp, created = TreeItem.objects.get_or_create(
        #     slug='na-raspredelenie',
        #     title='На распределение',
        # )
        # tmp.show = False
        # if created:
        #     tmp.save()

        # if obj.id != tmp.id:
        #     obj.move_to(tmp, 'last-child')

    def get_form(self, request, obj=None, **kwargs):
        """ Метод возвращает класс формы, переопределим метод валидации слага
        при создании нового элемента курса, проверяя наличие такого слага на данном уровне дерева"""
        # TODO не самое изящное решение, переделать

        FormClass = super(TreeItemFlatAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormCatalogWrapper(FormClass):

            def clean_slug(self):
                slug = self.cleaned_data['slug']
                if obj is None:
                    node = None
                    target = None
                    position = 'last-child'
                else:
                    node = obj
                    target = node
                    position = 'left'
                target_id = request.GET.get('target', None)
                copy_id = request.GET.get('copy', None)
                if target_id or copy_id:
                    try:
                        if target_id:
                            target = TreeItem.objects.get(pk=target_id)
                        elif copy_id:
                            target = TreeItem.objects.get(pk=copy_id).parent
                    except TreeItem.DoesNotExist:
                        pass
                    position = 'last-child'
                if not TreeItem.check_slug(target, position, slug, node):
                    message = 'На данном уровне есть элемент с таким-же слагом: "%s"' % self.cleaned_data['slug']
                    raise forms.ValidationError(message)
                return slug

        return ModelFormCatalogWrapper


admin.site.register(TreeItemFlat, TreeItemFlatAdmin)
