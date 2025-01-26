from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, matric_id, email, password=None, **extra_fields):
        if not matric_id:
            raise ValueError('The Matric ID field must be set')
        email = self.normalize_email(email)
        user = self.model(matric_id=matric_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matric_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superadmin')

        return self.create_user(matric_id, email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Remove the default username field
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('staff', 'University Staff'),
        ('admin', 'Admin'),
        ('superadmin', 'Superadmin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    matric_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    hostel_block = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'matric_id'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.matric_id} ({self.get_role_display()})"
