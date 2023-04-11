from django.shortcuts import render, redirect
from django.http import HttpResponse


def appindex(request):
    # return HttpResponse("<h1>This is the home page</h1>")
    return render(
        request,
        "appindex.html",
        {},
    )
