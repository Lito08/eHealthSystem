from django.core.management.base import BaseCommand
from django.utils.timezone import now
from appointments.models import Appointment

class Command(BaseCommand):
    help = "Automatically mark past appointments as Completed"

    def handle(self, *args, **kwargs):
        current_time = now().time()
        current_date = now().date()

        appointments = Appointment.objects.filter(
            appointment_date__lt=current_date,
            status='Scheduled'
        )

        for appointment in appointments:
            appointment.status = 'Completed'
            appointment.save()
            self.stdout.write(self.style.SUCCESS(f'Appointment {appointment.appointment_id} marked as Completed.'))

        # Handle same-day past appointments
        same_day_appointments = Appointment.objects.filter(
            appointment_date=current_date,
            appointment_time__lt=current_time,
            status='Scheduled'
        )

        for appointment in same_day_appointments:
            appointment.status = 'Completed'
            appointment.save()
            self.stdout.write(self.style.SUCCESS(f'Same-day Appointment {appointment.appointment_id} marked as Completed.'))
