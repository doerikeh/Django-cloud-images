from django.urls import path
from .views import PictureList,SearchView, upload_picture, PictureDetail, change_picture, delete_picture, add_picture

app_name = "picture"

urlpatterns = [
    path("", PictureList.as_view(), name="img-list"),
    path("add/", add_picture, name="add"),
    path("upload/", upload_picture, name="upload"),
    path("picture/<int:pk>/", PictureDetail.as_view(), name="detail"),
    path("picture/<int:pk>/change/", change_picture, name="edit_picture"),
    path("picture/<str:filename>/delete/", delete_picture, name="delete"),
    path("search/", SearchView.as_view(), name="search")
]