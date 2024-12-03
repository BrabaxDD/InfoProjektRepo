from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello World")


def game(request):
    context = {"content": "Willkommen im Djungel"}
    return render(request, "index.html", context)
