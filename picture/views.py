from django.shortcuts import render
from .models import Picture


def home(request):
    return render(request, "home.html", {})