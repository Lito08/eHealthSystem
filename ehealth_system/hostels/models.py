from django.db import models
from django.conf import settings

class Hostel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    block = models.CharField(max_length=50)
    levels = models.PositiveIntegerField()
    rooms_per_level = models.PositiveIntegerField()

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
        return self.name

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="rooms")
    number = models.CharField(max_length=20, unique=True)
    resident = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_occupied(self):
        return self.resident is not None

    def __str__(self):
        return f"{self.hostel.name} - {self.number} ({'Occupied' if self.is_occupied else 'Available'})"
