from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class MusicFile(models.Model):
    UPLOAD_CHOICES = [
        ('public', 'Public'),       # Option for public visibility
        ('private', 'Private'),     # Option for private visibility
        ('protected', 'Protected'), # Option for protected visibility
    ]

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # ForeignKey to the user who uploaded the music file
    file = models.FileField(upload_to='allmusic/')
    # FileField to store the uploaded music file
    visibility = models.CharField(max_length=10, choices=UPLOAD_CHOICES)
    # CharField to specify the visibility of the music file
    allowed_emails = models.TextField(blank=True)
    # TextField to store the allowed emails for protected visibility

    def has_access(self, email):
        if self.visibility == 'public':
            return True
        elif self.visibility == 'private':
            return self.uploader.email == email
        elif self.visibility == 'protected':
            allowed_emails = [e.strip() for e in self.allowed_emails.split(',')]
            return email in allowed_emails
    # Method to check if a given email has access to the music file
