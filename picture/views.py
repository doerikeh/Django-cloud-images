from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Picture
from user.models import Project
from django.db.models import Q

from django.views.generic import ListView
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from itertools import chain
from .forms import ImageUpload

class PictureList(ListView):
    model = Picture
    queryset = Picture.objects.all()
    context_object_name = "picture_list"
    template_name = "home.html"
    redirect_field_name = "user/login/"
    paginate_by = 20


class SearchView(ListView):
    template_name = "search.html"
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context["query"] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            project_result = Project.objects.search(query)
            picture_result = Picture.objects.search(query)

            queryset_chain = chain(
                project_result,
                picture_result
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)
            return qs
        return Picture.objects.none()

def save_upload_file_to_media_root(f):
    with open('%s%s' % (settings.MEDIA_ROOT, f.name), "wb+") as picture_img:
        for chunk in f.chunks():
            picture_img.write(chunk)

def upload(request):
    if request.method == "POST":
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.user = request.user
            picture.save()
    else:
        form = ImageUpload()
    return render(request, "upload_image.html", {"pictures":form})
        