from django.urls import path
from .views import PictureList,SearchView, upload, PictureDetail, add_or_change_picture, delete_picture

app_name = "picture"

urlpatterns = [
    path("", PictureList.as_view(), name="img-list"),
    path("upload/", upload, name="upload"),
    path("picture/<pk>/", PictureDetail.as_view(), name="detail"),
    path("<uuid:pk>/change/", add_or_change_picture, name="change"),
    path("<uuid:pk>/delete/", delete_picture, name="delete"),
    path("search/", SearchView.as_view(), name="search")
]