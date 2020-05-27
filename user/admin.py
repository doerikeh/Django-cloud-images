from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AdminUser
from .models import User, Profile, Project
from django.utils.html import format_html


@admin.register(User)
class Users(AdminUser):
    fieldsets = (
        (None, {"fields":("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name",)},),
        ("Permission", {"fields":("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},),
        ("Important date", {"fields": ("last_login", "date_joined")},),
    )
    
    add_fieldsets = (
        (None, {"classes":("wide",),"fields":("email", "password1", "password2"),},),
    )


    list_filter = ("is_staff", "is_superuser", "is_active")
    list_display_links = ("email",)
    list_display = ("email","is_staff" , "last_login",)
    search_fields = ("email", "first_name", "last_name", )
    ordering = ("email",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "images", "username", "date_created")
    search_fields = ("username",)
    list_filter = ("date_created",)

    def images(self, obj):
        if obj.image:
            return format_html(
                '<img src="%s" width="100" heigth="100" />' % obj.image.url
            )
        return ""
    images.short_description = "User"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "date_created", "tags")
    list_filter = ("date_created",)
    search_fields = ("title", "tags",)