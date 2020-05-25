from django.contrib.auth.forms import (
 UserCreationForm as DjangoUserCreationForm
)
from django.core.mail import send_mail
import logging
from django.contrib.auth.forms import UsernameField
from .models import User
logger = logging.getLogger(__name__)


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": UsernameField}
        def send_mail(self):
            logger.info(
            "Sending signup email for email=%s",
            self.cleaned_data["email"],
            )
            message = "Welcome{}".format(self.cleaned_data["email"])
            send_mail(
                "Welcome to Cloudimage",
                message,
                "site@climage.domain",
                [self.cleaned_data["email"]],
                fail_silently=True,
            )