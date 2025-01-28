from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import datetime

class CustomUserManager(BaseUserManager):
    def generate_matric_id(self, role):
        year = datetime.now().year % 100  # Get last two digits of the current year
        prefix = {
            'admin': 'A',
            'staff': 'UC',
            'lecturer': 'L',
            'student': 'S'
        }.get(role, 'S')
        
        last_user = self.model.objects.filter(role=role).order_by('-matric_id').first()
        if last_user and last_user.matric_id:
            last_number = int(last_user.matric_id[3:]) + 1
        else:
            last_number = 1

        return f"{prefix}{year}{last_number:04d}"

    def create_user(self, matric_id=None, email=None, password=None, **extra_fields):
        if not matric_id:
            matric_id = self.generate_matric_id(extra_fields.get('role', 'student'))
        email = self.normalize_email(email)
        user = self.model(matric_id=matric_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matric_id=None, email=None, password=None, **extra_fields):
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
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'matric_id'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.role == 'superadmin':
            self.full_name = ''  # Automatically blank name for superadmins
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.matric_id} ({self.get_role_display()})"
