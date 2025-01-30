from django.db import models
from django.conf import settings
from datetime import timedelta, date


class Hostel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    block = models.CharField(max_length=50)
    levels = models.PositiveIntegerField()
    rooms_per_level = models.PositiveIntegerField()
    is_infected_hostel = models.BooleanField(default=False)  # Flag for quarantine hostels

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_rooms()

    def generate_rooms(self):
        """Automatically generate rooms based on levels and rooms per level."""
        for level in range(1, self.levels + 1):
            for room_no in range(1, self.rooms_per_level + 1):
                room_number = f"{self.block}-{level:02d}{room_no:02d}"
                Room.objects.get_or_create(hostel=self, number=room_number)

    def __str__(self):
        return f"{self.name} ({'Quarantine' if self.is_infected_hostel else 'Regular'})"


class Room(models.Model):
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        related_name="rooms"
    )
    number = models.CharField(max_length=20, unique=True)
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_room"
    )

    @property
    def is_occupied(self):
        return self.resident is not None

    @staticmethod
    def find_available_quarantine_room():
        """Finds an available room in an infected hostel for quarantine."""
        return Room.objects.filter(hostel__is_infected_hostel=True, resident__isnull=True).first()

    @staticmethod
    def find_available_normal_room():
        """Finds an available normal room for recovered residents."""
        return Room.objects.filter(hostel__is_infected_hostel=False, resident__isnull=True).first()

    def __str__(self):
        return f"{self.hostel.name} - {self.number} ({'Occupied' if self.is_occupied else 'Available'})"


class ResidentHealthStatus(models.Model):
    """Tracks infected residents and their original rooms for relocation after recovery."""
    resident = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="health_status"
    )
    original_room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="previously_assigned"
    )
    infected_since = models.DateField(null=True, blank=True)

    def is_infected(self):
        """Checks if a resident is still infected (less than 14 days since infection)."""
        if self.infected_since:
            return (date.today() - self.infected_since) < timedelta(days=14)
        return False

    def recover_resident(self):
        """Moves the resident back to their original room after recovery."""
        if self.original_room and not self.original_room.is_occupied:
            self.original_room.resident = self.resident
            self.original_room.save()

            # Reset health status
            self.original_room = None
            self.infected_since = None
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.resident.full_name} - {'Infected' if self.is_infected() else 'Recovered'}"
