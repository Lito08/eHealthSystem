from django.db import models

class Resident(models.Model):
    RESIDENT_TYPE_CHOICES = [
        ('Student', 'Student'),
        ('Lecturer', 'Lecturer'),
        ('Staff', 'Staff'),
    ]
    name = models.CharField(max_length=100)
    resident_id = models.CharField(max_length=20, unique=True)
    resident_type = models.CharField(max_length=10, choices=RESIDENT_TYPE_CHOICES)

    def __str__(self):
        return self.name

class HealthStatus(models.Model):
    STATUS_CHOICES = [
        ('Healthy', 'Healthy'),
        ('Infected', 'Infected'),
    ]
    resident = models.OneToOneField(Resident, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    report_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resident.name} - {self.status}"

class QuarantineRoom(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    resident = models.OneToOneField(Resident, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return f"Room {self.room_number} - {self.resident.name}"

# Create your models here.
