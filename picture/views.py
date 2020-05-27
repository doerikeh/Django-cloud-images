from django.shortcuts import render
from .models import Picture
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q


class PictureList(ListView):
    model = Picture
    queryset = Picture.objects.all()
    context_object_name = "picture_list"
    template_name = "home.html"
    paginate_by = 20


def search(request):
    if request.method == "GET":
        pictures = request.GET.get("search", '')
        try:
            status = Picture.objects.filter(Q(user__email__icontains=pictures) |
                                        Q(deskripsi__icontains=pictures))
        except Picture.DoesNotExist:
            status = None
        return render(request, "search.html", {"picture":status})
    else:
        return render(request, "search.html",{})
        
