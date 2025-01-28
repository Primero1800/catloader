from django.http import HttpResponse
from django.shortcuts import render

from .tasks import addff

def home(request):
    addff.delay(1, 2)

    return HttpResponse(
        '<h1>Хайло</h1>'
    )
