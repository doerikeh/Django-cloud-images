from django.contrib import admin
from .models import Picture

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ("user", "img", "date_created", "date_updated")
    list_filter = ("date_created", "date_updated")