from django.db import models
from user.models import User
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
import os
from PIL import Image

from django.conf import settings
from django.core.files.storage import default_storage as storage

THUMBNAIL_SIZE =  getattr(settings, "PICTURE_THUMBNAIL_SIZE", 50)
THUMBNAIL_EXT = getattr(settings, "PICTURE_THUMBNAIL_EXT", None)


def get_image_crop_points(image):
    width, heigth = image.size
    target = width if width > heigth else heigth
    upper, lower = get_centering_points(heigth, target)
    left, right = get_centering_points(width, target)
    return left, right, upper, lower

def get_centering_points(size, target):
    delta = size - target
    start = int(delta) / 2
    end = start + target
    return start, end


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_thumbnail()
    
    def create_thumbnail(self):
        if not self.img:
            return False
        picture_path, thumbnail_path = self.get_picture_path()
        if thumbnail_path and not storage.exists(thumbnail_path):
            try:
                picture_file = storage.open(picture_path, "r")
                image = Image.open(picture_file)
                image = Image.crop(get_image_crop_points(image))
                image = Image.resize(THUMBNAIL_SIZE, THUMBNAIL_SIZE, Image.ANTIALIAS)
                image.save(thumbnail_path)
            except(IOError, KeyError, UnicodeDecodeError):
                return False
        return True

    def get_thumbnail_picture_path(self):
        url = ""
        picture_path, thumbnail_path = self.get_picture_path()  
        if thumbnail_path:
            url = (storage.url(thumbnail_path) if storage.exists(thumbnail_path) else self.img.url)
        return url
    def get_picture_path(self):
        picture_path = None
        thumb_path = None

        if self.img:
            picture_path = self.img.name
            filename_base, filename_ext =os.path.splitext(
                picture_path
            )
            if THUMBNAIL_EXT:
                filename_ext = THUMBNAIL_EXT
            thumb_path = f"{filename_base}_thumbnail{filename_ext}"
        return picture_path, thumb_path
