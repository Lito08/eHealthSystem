from django.core.management.base import BaseCommand
from users.models import CustomUser
from appointments.models import Appointment
from django.utils.timezone import now
from datetime import timedelta

class Command(BaseCommand):
    help = "Marks infected residents as recovered after 2 weeks and relocates them."

    def handle(self, *args, **kwargs):
        two_weeks_ago = now().date() - timedelta(days=14)

        # Find infected residents whose appointment is older than 14 days
        infected_residents = CustomUser.objects.filter(
            infected_status="infected",
            appointments__result="Positive",
            appointments__appointment_date__lte=two_weeks_ago
        ).distinct()

        for resident in infected_residents:
            if resident.original_room:
                # Move back to the original room
                original_room = resident.original_room
                original_room.resident = resident
                original_room.save()

                # Free up the quarantine room
                if resident.room:
                    resident.room.resident = None
                    resident.room.save()

                # Update resident status
                resident.infected_status = "recovered"
                resident.room = resident.original_room  # Relocate back
                resident.original_room = None  # Clear saved room
                resident.save()

                self.stdout.write(self.style.SUCCESS(f"{resident.full_name} has recovered and returned to their original room."))
