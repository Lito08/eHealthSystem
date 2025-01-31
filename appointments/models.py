import uuid
from datetime import time
from django.db import models, IntegrityError
from django.conf import settings
from django.utils.timezone import now
from hostels.models import Room, ResidentHealthStatus

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    RESULT_CHOICES = [
        ('Pending', 'Pending'),
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
    ]

    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Confirmed', 'Confirmed'),
    ]

    appointment_id = models.CharField(max_length=50, unique=True, blank=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(default=time(12, 0))
    resident = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default="Pending")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Scheduled")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['appointment_date', 'appointment_time', 'clinic'],
                name='unique_clinic_appointment'
            )
        ]

    def save(self, *args, **kwargs):
        """Automatically assign an appointment ID if not provided."""
        if not self.appointment_id:
            self.appointment_id = "APPT" + str(uuid.uuid4().hex[:8]).upper()
        super().save(*args, **kwargs)

    def confirm_appointment(self):
        """Mark an appointment as confirmed."""
        self.status = "Confirmed"
        self.save()

    def mark_completed(self, result):
        """
        Mark appointment as completed and handle infection logic.
        - If Positive: Move resident to quarantine.
        - If Negative: No change in residence.
        """
        if result not in ['Positive', 'Negative']:
            raise ValueError("Invalid result type. Must be 'Positive' or 'Negative'.")

        self.result = result
        self.status = "Completed"
        self.save()

        if result == "Positive":
            self.handle_infected_resident()

    def handle_infected_resident(self):
        """Handles the relocation of an infected resident."""
        resident = self.resident
        health_status, created = ResidentHealthStatus.objects.get_or_create(resident=resident)

        # If already marked infected, do nothing
        if resident.infected_status == "infected":
            return

        # Save original room before relocation
        health_status.original_room = resident.assigned_room
        health_status.infected_since = now().date()
        health_status.save()

        # Move resident to quarantine room
        quarantine_room = Room.find_available_quarantine_room()
        if quarantine_room:
            if resident.assigned_room:
                resident.assigned_room.resident = None
                resident.assigned_room.save()

            resident.assigned_room = quarantine_room
            resident.infected_status = "infected"
            resident.save()

            quarantine_room.resident = resident
            quarantine_room.save()

    def __str__(self):
        return f"{self.resident.matric_id} - {self.clinic.name} on {self.appointment_date} at {self.appointment_time}"
