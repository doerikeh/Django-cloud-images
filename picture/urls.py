from django.urls import path
from .views import PictureList, search

app_name = "picture"

urlpatterns = [
    path("", PictureList.as_view(), name="img-list"),
    path("search/", search, name="search")
]