from django.urls import path
from .views import SingupView, profile
from .forms import AuthenticatedForm
from django.contrib.auth import views as auth_views

app_name = "user"

urlpatterns = [
    path("profile/", profile, name="profile"),
    
    path("register/", SingupView.as_view(), name='register'),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", form_class=AuthenticatedForm), name="login"),
]