from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.db.models import Q



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError("Harus Menggunakan Email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_field):
        extra_field.setdefault("is_staff", False)
        extra_field.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_field)


    def create_superuser(self, email, password=None, **extra_field):
        extra_field.setdefault("is_staff", True)
        extra_field.setdefault("is_superuser", True)
        if extra_field.get("is_staff") is not True:
            raise ValueError(
            "superuser must have is_staff=True"
        )
        if extra_field.get("is_superuser") is not True:
            raise ValueError(
            "superuser must have is_superuser=True"
        )
        return self._create_user(email, password, **extra_field)
        

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    def __str__(self):
        return f"{self.email}"

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Image %Y/%m/%d')
    username = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class ProjectQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(deskripsi__icontains=query)|
                        Q(title__icontains=query)|
                        Q(tags__name__icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs

class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)
    def search(self, query=None):
        return self.get_queryset().search(query=query)
class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, db_constraint=False)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    tags = TaggableManager()
    deskripsi = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    objects = ProjectManager()

    def __str__(self):
        return self.title