from django.db import models
from django.contrib.auth.models import User
from datetime import time  # Import the correct time format

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    appointment_id = models.CharField(max_length=50, unique=True, default="DEFAULT_APPT")
    appointment_date = models.DateField()
    appointment_time = models.TimeField(default=time(12, 0))  # Use proper time object
    resident = models.ForeignKey(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    result = models.TextField(blank=True, null=True)  # Added based on class diagram
    status = models.CharField(max_length=20, choices=[
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Confirmed', 'Confirmed'),
    ], default='Scheduled')
    
    def confirm_appointment(self):
        self.status = "Confirmed"
        self.save()

    def __str__(self):
        return f"{self.resident.username} - {self.clinic.name} on {self.appointment_date}"
