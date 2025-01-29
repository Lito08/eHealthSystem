from django.db import models

class Hotspot(models.Model):
    location_name = models.CharField(max_length=255, unique=True)
    infected_count = models.IntegerField(default=0)
    recovered_count = models.IntegerField(default=0)
    latitude = models.FloatField(null=True, blank=True)  # Latitude for mapping
    longitude = models.FloatField(null=True, blank=True)  # Longitude for mapping
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location_name} - Infected: {self.infected_count}, Recovered: {self.recovered_count}"
