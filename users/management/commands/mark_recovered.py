from django.core.management.base import BaseCommand
from users.models import CustomUser
from hostels.models import Room, ResidentHealthStatus
from django.utils.timezone import now
from datetime import timedelta

class Command(BaseCommand):
    help = "Marks infected residents as recovered after 2 weeks and relocates them."

    def handle(self, *args, **kwargs):
        two_weeks_ago = now().date() - timedelta(days=14)

        # Find infected residents who tested positive more than 14 days ago
        infected_residents = CustomUser.objects.filter(
            infected_status="infected",
            health_status__infected_since__lte=two_weeks_ago
        ).distinct()

        for resident in infected_residents:
            health_status = resident.health_status

            if health_status and health_status.original_room and not health_status.original_room.is_occupied():
                # Move resident back to their original room
                original_room = health_status.original_room
                original_room.resident = resident
                original_room.save()

                # Free up the quarantine room (if any)
                quarantine_room = resident.rooms_assigned.first()
                if quarantine_room:
                    quarantine_room.resident = None
                    quarantine_room.save()

                # Update resident's health status
                resident.infected_status = "recovered"
                resident.rooms_assigned.set([original_room])  # Assign back original room
                health_status.original_room = None  # Reset saved original room
                health_status.infected_since = None  # Reset infection date
                resident.save()
                health_status.save()

                self.stdout.write(self.style.SUCCESS(f"{resident.full_name} has recovered and returned to their original room."))
            else:
                self.stdout.write(self.style.WARNING(f"{resident.full_name} could not be relocated. Their original room may be occupied."))
