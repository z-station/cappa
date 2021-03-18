import re
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.conf.urls import url
from django.core.exceptions import PermissionDenied

from adminsortable2.admin import SortableAdminMixin
from app.training.models import Course, Topic
from app.training.admin import TopicInline, TopicAdmin

IS_POPUP_VAR = '_popup'
TO_FIELD_VAR = '_to_field'

HORIZONTAL, VERTICAL = 1, 2


@admin.register(Course)
class CourseAdmin(SortableAdminMixin, admin.ModelAdmin):

    model = Course
    list_display = ('order_key', 'title', 'author', 'show')
    list_display_links = ('title',)
    fields = ('show', 'title', 'slug', 'translator', 'author', 'about', 'content', 'content_bottom')
    prepopulated_fields = {'slug': ['title']}
    inlines = [TopicInline]
    raw_id_fields = ("author",)

    def set_instance(self, request):
        object_id = re.search(r'\d+', request.META['PATH_INFO']).group(0)
        self.instance = self.model.objects.get(pk=object_id)

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        if not obj:
            for inline in inline_instances:
                if inline.__class__ == TopicInline:
                    inline_instances.remove(inline)
        return inline_instances

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.set_instance(request)
        return self.changeform_view(request, object_id, form_url, extra_context)

    def get_object_with_change_permissions(self, request, model, obj_pk):
        obj = get_object_or_404(model, pk=obj_pk)
        if not self.has_change_permission(request, obj):
            raise PermissionDenied
        return obj

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial.update({
            'author': request.user,
            'order_key': Course.objects.all().count() + 1
        })
        return initial

    def add_topic(self, request, course_pk):
        course = self.get_object_with_change_permissions(request, Course, course_pk)
        topic_admin = TopicAdmin(Topic, self.admin_site, course)
        return topic_admin.add_view(request, extra_context={'course': course})

    def change_topic(self, request, course_pk, topic_pk):
        course = self.get_object_with_change_permissions(request, Course, course_pk)
        topic_admin = TopicAdmin(Topic, self.admin_site, course)
        return topic_admin.change_view(request, object_id=topic_pk, extra_context={'course': course})

    def get_urls(self):
        return [
            url(r'^(?P<course_pk>[0-9]+)/topics/add/$', self.admin_site.admin_view(self.add_topic), name='add_topic'),
            url(r'^(?P<course_pk>[0-9]+)/topics/(?P<topic_pk>[0-9]+)/change/$', self.admin_site.admin_view(self.change_topic), name='change_topic'),
        ] + super().get_urls()

