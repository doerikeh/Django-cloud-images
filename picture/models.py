from django.db import models
from user.models import User
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
import os



def upload(instance, filename):
    now = timezone_now()
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    return f"picture/{now:%Y/%m/%Y%m%d%H%M%S}{ext}"


class PictureQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(deskripsi__icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs

class PictureManager(models.Manager):
    def get_queryset(self):
        return PictureQuerySet(self.model, using=self._db)
    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=upload)
    deskripsi = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = PictureManager()


    def __str__(self):
        return self.user.email