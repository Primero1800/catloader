from django.http import HttpResponse
from django.shortcuts import render

from .tasks import add_ff, import_image_of_cat


def home(request):

    add_ff.delay(1, 2)
    import_image_of_cat.delay()

    return HttpResponse(
        '<h1>Хайло</h1>'
    )
