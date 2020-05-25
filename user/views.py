from django.shortcuts import render
import logging
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.generic.edit import FormView
from .form import UserCreationForm

logger = logging.getLogger(__name__)

class SingupView(FormView):
    template_name = "singup.html"
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
            self.request, "YOu Singup success"
        )
        return response