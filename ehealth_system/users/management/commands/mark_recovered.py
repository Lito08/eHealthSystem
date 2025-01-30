from django.core.management.base import BaseCommand
from users.models import CustomUser
from appointments.models import Appointment
from django.utils.timezone import now
from datetime import timedelta

class Command(BaseCommand):
    help = "Marks infected residents as recovered after 2 weeks and relocates them."

    def handle(self, *args, **kwargs):
        two_weeks_ago = now().date() - timedelta(days=14)

        infected_residents = CustomUser.objects.filter(
            infected_status="infected",
            appointment__result="Positive",
            appointment__appointment_date__lte=two_weeks_ago
        ).distinct()

        for resident in infected_residents:
            resident.mark_recovered()

        self.stdout.write(self.style.SUCCESS(f"Recovered {infected_residents.count()} residents."))
