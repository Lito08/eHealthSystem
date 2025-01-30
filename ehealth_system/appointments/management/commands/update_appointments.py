from django.core.management.base import BaseCommand
from appointments.models import Appointment
from datetime import datetime
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Automatically mark past scheduled appointments as 'Completed'"

    def handle(self, *args, **kwargs):
        current_time = now()

        # Find all scheduled appointments where the date/time is in the past
        past_appointments = Appointment.objects.filter(
            status='Scheduled',
            appointment_date__lt=current_time.date()
        ) | Appointment.objects.filter(
            status='Scheduled',
            appointment_date=current_time.date(),
            appointment_time__lt=current_time.time()
        )

        # Update the status to 'Completed'
        updated_count = past_appointments.update(status='Completed')

        self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} past appointments to 'Completed'."))
