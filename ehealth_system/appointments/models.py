import uuid
from datetime import time
from django.db import models, IntegrityError
from django.conf import settings

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    appointment_id = models.CharField(max_length=50, unique=True, blank=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(default=time(12, 0))
    resident = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    result = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Confirmed', 'Confirmed'),
    ], default='Scheduled')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['appointment_date', 'appointment_time', 'clinic'],
                name='unique_clinic_appointment'
            )
        ]

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            self.appointment_id = "APPT" + str(uuid.uuid4().hex[:8]).upper()
        super().save(*args, **kwargs)

    def confirm_appointment(self):
        self.status = "Confirmed"
        self.save()

    def __str__(self):
        return f"{self.resident.matric_id} - {self.clinic.name} on {self.appointment_date} at {self.appointment_time}"
