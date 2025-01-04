from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("0000000000000000000000000000000\n111111111111111111111111111111\n0000000000000000000000000000000\n1111111111111111111111111111111")


def game(request):
    context = {"content": "Willkommen im Djungel"}
    return render(request, "index.html", context)
