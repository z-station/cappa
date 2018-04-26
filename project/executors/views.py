from django.views import View
from django.shortcuts import HttpResponse


def execute(request):
    return HttpResponse("execute")
