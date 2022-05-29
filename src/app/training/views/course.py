# -*- coding:utf-8 -*-
from django.shortcuts import render, Http404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from app.training.models import Course


class CourseListView(View):

    def get(self, request, *args, **kwargs):
        return render(
            template_name='training/courses.html',
            context={'objects': Course.objects.filter(show=True)},
            request=request
        )


@method_decorator(login_required, name='dispatch')
class CourseView(View):

    def get_object(self, request, *args, **kwargs):
        try:
            return Course.objects.get(slug=kwargs['course'])
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        course = self.get_object(request, *args, **kwargs)
        return render(
            template_name='training/course.html',
            context={
                'object': course,
                'course': course,
            },
            request=request
        )

