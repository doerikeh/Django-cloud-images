from django.db import models
from user.models import User

from django.db.models import Q

class PictureManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(deskripsi__icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs


class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="picture/%Y/%m/%d")
    deskripsi = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = PictureManager()


    def __str__(self):
        return self.user.email