# -*- coding:utf-8 -*-
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from src.training.forms import ContentForm
from src.training.models import Topic


@method_decorator(login_required, name='dispatch')
class TopicView(View):

    def get_object(self, request, *args, **kwargs):
        try:
            return Topic.objects.select_related('course__lang')\
                .get(slug=kwargs['topic'], course__slug=kwargs['course'])
        except Topic.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        topic = self.get_object(request, *args, **kwargs)
        return render(
            request=request,
            template_name='training/topic/template.html',
            context={
                'object': topic,
                'course': topic.course,
            }
        )

    def post(self, request, *args, **kwargs):
        topic = self.get_object(request, *args, **kwargs)
        form = ContentForm(data=request.POST)
        response = form.perform_operation(topic)
        return JsonResponse(response.__dict__)