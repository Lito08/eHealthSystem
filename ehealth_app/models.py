from django.contrib.auth.models import AbstractUser
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('Resident', 'Resident'),
        ('Admin', 'Admin'),
        ('Clinic', 'Clinic'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    # Override groups and user_permissions with unique related names
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Unique related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
