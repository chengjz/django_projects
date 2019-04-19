from django import forms
from horses.models import Horse
from django.core.files.uploadedfile import InMemoryUploadedFile
from horses.humanize import naturalsize

from django.core.exceptions import ValidationError
from django.core import validators

# Create the form class.
class CreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)


    class Meta:
        model = Horse
        fields = ['name', 'height', 'weight']  # Picture is manual


class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
