# -*- coding:utf-8 -*-
from django.shortcuts import render, Http404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from src.quizzes.models import Quiz


class QuizListView(View):

    def get(self, request, *args, **kwargs):
        return render(
            template_name='quizzes/quiz_list.html',
            context={'objects': Quiz.objects.filter(show=True)},
            request=request
        )


@method_decorator(login_required, name='dispatch')
class QuizView(View):

    def get_object(self, request, *args, **kwargs):
        try:
            return Quiz.objects.select_related('lang').get(slug=kwargs['quiz'])
        except Quiz.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        quiz = self.get_object(request, *args, **kwargs)
        return render(
            template_name='quizzes/quiz.html',
            context={
                'object': quiz,
                'quiz': quiz,
            },
            request=request
        )

