from django.shortcuts import render
from .models import Picture
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404


class PictureList(ListView):
    model = Picture
    queryset = Picture.objects.all()
    context_object_name = "picture_list"
    template_name = "home.html"
    paginate_by = 20
