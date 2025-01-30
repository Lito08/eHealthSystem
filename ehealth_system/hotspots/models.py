from django.db import models

class Hotspot(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Unique hotspot name
    description = models.TextField(blank=True, null=True)  # Optional description
    infected_count = models.PositiveIntegerField(default=0)  # Positive number only
    recovered_count = models.PositiveIntegerField(default=0)  # Positive number only
    latitude = models.FloatField(null=True, blank=True)  # Required for mapping
    longitude = models.FloatField(null=True, blank=True)  # Required for mapping
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Infected: {self.infected_count}, Recovered: {self.recovered_count}"
