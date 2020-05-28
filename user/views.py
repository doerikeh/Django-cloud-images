from django.shortcuts import render, get_object_or_404
import logging
from django.contrib.auth import login, authenticate

from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import UserCreationForm, ProjectForm
from .models import Profile, Project
from taggit.models import Tag
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.template.defaultfilters import slugify



logger = logging.getLogger(__name__)

class SingupView(FormView):
    template_name = "register.html"
    form_class = UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info(
            "New Singup for email=%s", email
        )
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        form.send_mail()
        messages.info(
            self.request, "You Singup success"
        )
        return response

def profile(request, slug=None):
    profile = Profile.objects.all()
    project = Project.objects.order_by("-date_created")
    form  = ProjectForm(request.POST)
    if form.is_valid():
        newproject = form.save(commit=False)
        newproject.save()
        form.save_m2m()

    context = {
        'profile':profile,
        "project_list": project,
        "form": form
    }
    return render (request, "profile.html", context)

