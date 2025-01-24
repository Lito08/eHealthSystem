from django.test import TestCase
from django.contrib.auth.models import User
from .models import Appointment, Clinic
from django.utils.timezone import now

class AppointmentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.clinic = Clinic.objects.create(name="Clinic A", contact_info="clinic@example.com")

    def test_appointment_creation(self):
        appointment = Appointment.objects.create(
            resident=self.user,
            clinic=self.clinic,
            appointment_date=now(),
            status="Scheduled"
        )
        self.assertEqual(appointment.clinic.name, "Clinic A")
        self.assertEqual(appointment.resident.username, "testuser")
