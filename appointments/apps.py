from django.apps import AppConfig
from django.db.utils import OperationalError, IntegrityError


class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'

    def ready(self):
        """Populate initial clinic data when the app is ready."""
        from .models import Clinic
        try:
            if not Clinic.objects.exists():
                Clinic.objects.create(name="MMU Clinic", contact_info="clinic@mmu.edu.my")
                print("Clinic added successfully.")
        except (OperationalError, IntegrityError):
            # Handle case where migrations have not been applied yet
            print("Skipping data population, apply migrations first.")
