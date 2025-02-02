from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import datetime, timedelta, date
from hostels.models import Room
from django.contrib import messages

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
    username = None
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
    infected_status = models.CharField(
        max_length=20,
        choices=[('healthy', 'Healthy'), ('infected', 'Infected'), ('recovered', 'Recovered')],
        default='healthy'
    )
    original_room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="original_room_residents"
    )
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="current_residents"
    )

    USERNAME_FIELD = 'matric_id'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def mark_infected(self, request):
        """Moves an infected resident to a quarantine room."""
        quarantine_room = Room.find_available_quarantine_room()
        if quarantine_room:
            # ✅ Store original room before moving to quarantine
            if self.room:
                self.original_room = self.room  

            self.room = quarantine_room
            self.infected_status = 'infected'
            self.save()

            # ✅ Assign the resident to the new room
            quarantine_room.resident = self
            quarantine_room.save()

            messages.success(request, f"{self.full_name} has been relocated to quarantine.")
        else:
            messages.warning(request, "No available quarantine rooms.")

    def mark_recovered(self, request):
        """Moves a recovered resident back to their original room if available."""
        if not self.original_room:
            messages.warning(request, f"{self.full_name} has no original room recorded.")
            return  

        if self.room:
            # ✅ Free up the current (quarantine) room
            self.room.resident = None
            self.room.save()

        # ✅ Check if the original room is occupied
        if self.original_room.resident is None:
            self.room = self.original_room
            self.original_room.resident = self
            self.original_room.save()

            # ✅ Reset fields
            self.infected_status = "healthy"  # ✅ Updated to 'healthy'
            self.original_room = None
            self.save()

            messages.success(request, f"{self.full_name} has recovered and returned to their original room.")
        else:
            messages.warning(request, f"{self.full_name} cannot return. Their original room is occupied.")

    def save(self, *args, **kwargs):
        if self.role == 'superadmin':
            self.full_name = ''
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.matric_id} ({self.get_role_display()})"
