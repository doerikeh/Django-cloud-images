from django import forms
from .models import Picture
from django.forms.renderers import TemplatesSetting
import os
from .storage import upload_storage


class ImageUpload(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ("img", "deskripsi",)
        img_path = forms.CharField(max_length=255, widget=forms.HiddenInput(), required=False)

    def save(self, commit=True):
        instance = super().save(commit=commit)
        img = self.cleaned_data("img")
        path = self.cleaned_data("img_path")
        if not img and path:
            try:
                img = upload_storage.open(path)
                instance.img.save(path, img, False)
                os.remove(path)
            except FileNotFoundError:
                pass
        instance.save()
        return instance
