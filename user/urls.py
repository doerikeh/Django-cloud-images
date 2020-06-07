from django.urls import path
from .views import SingupView, profile
from .forms import AuthenticatedForm
from django.contrib.auth import views as auth_views

app_name = "user"

urlpatterns = [
    path("profile/", profile, name="profile"),
    
    path("register/", SingupView.as_view(), name='register'),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", form_class=AuthenticatedForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="password_change_form.html"), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="password_change_done.html"), name="password_change_done"),

    path("password_reset/",auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confrim.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complate.html"), name="password_reset_complete")
]