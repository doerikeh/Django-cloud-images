from django.contrib import admin
from django.utils.html import format_html

from .models import Picture

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ("user", "image", "date_created", "date_updated")
    list_filter = ("date_created", "date_updated")

    def image(self, obj):
        if obj.img:
            return format_html(
                '<img src="%s" width="100" heigth="100" />' % obj.img.url
            )
        return ""
    image.short_description = "User"