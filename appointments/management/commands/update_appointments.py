from django.core.management.base import BaseCommand
from django.db.models import Q
from appointments.models import Appointment
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Automatically mark past scheduled appointments as 'Completed'"

    def handle(self, *args, **kwargs):
        current_time = now()

        # Find all scheduled appointments that are past the current date/time
        past_appointments = Appointment.objects.filter(
            Q(status='Scheduled') &
            (Q(appointment_date__lt=current_time.date()) |
             Q(appointment_date=current_time.date(), appointment_time__lt=current_time.time()))
        )

        # Log appointments being updated
        for appt in past_appointments:
            self.stdout.write(self.style.NOTICE(
                f"Updating appointment {appt.appointment_id} for {appt.resident.full_name} ({appt.resident.matric_id})"
            ))

        # Update the status to 'Completed'
        updated_count = past_appointments.update(status='Completed')

        if updated_count:
            self.stdout.write(self.style.SUCCESS(f"✅ {updated_count} past appointments marked as 'Completed'."))
        else:
            self.stdout.write(self.style.WARNING("⚠️ No past appointments found to update."))
