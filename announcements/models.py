from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title
