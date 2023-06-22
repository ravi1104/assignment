from django import forms
from .models import MusicFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = MusicFile
        fields = ['file', 'visibility', 'allowed_emails']
