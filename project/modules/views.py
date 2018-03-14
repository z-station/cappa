from django.shortcuts import render
from django.http import HttpResponse


def modules(request):
    return HttpResponse("modules")
