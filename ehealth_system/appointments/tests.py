from django.test import TestCase
from django.contrib.auth.models import User
from .models import Appointment, Clinic
from django.utils.timezone import now
from datetime import time

class AppointmentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpassword")
        cls.clinic = Clinic.objects.create(name="Clinic A", contact_info="clinic@example.com")

    def test_appointment_creation(self):
        appointment = Appointment.objects.create(
            appointment_id="APPT123",
            resident=self.user,
            clinic=self.clinic,
            appointment_date=now().date(),
            appointment_time=time(10, 0),  # Correct format for TimeField
            result="Pending"
        )
        self.assertEqual(appointment.clinic.name, "Clinic A")
        self.assertEqual(appointment.resident.username, "testuser")

    def test_confirm_appointment(self):
        appointment = Appointment.objects.create(
            appointment_id="APPT124",
            resident=self.user,
            clinic=self.clinic,
            appointment_date=now().date(),
            appointment_time=time(14, 0),  # Correct format for TimeField
            result="Pending"
        )
        appointment.confirm_appointment()
        self.assertEqual(appointment.status, "Confirmed")

        # Ensure changes were saved to the database
        updated_appointment = Appointment.objects.get(appointment_id="APPT124")
        self.assertEqual(updated_appointment.status, "Confirmed")
