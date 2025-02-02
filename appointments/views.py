from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment, Clinic
from users.models import CustomUser
from hostels.models import Hostel, Room, ResidentHealthStatus
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, time, timedelta
from django.utils.timezone import now

@login_required
def book_appointment(request):
    if request.user.role not in ['admin', 'superadmin']:
        messages.error(request, "You are not authorized to book appointments.")
        return redirect('appointment_list')

    clinic = Clinic.objects.first()  # Fetch the first clinic available

    if not clinic:
        messages.error(request, "No clinic available. Please contact admin.")
        return redirect('appointment_list')

    current_time = now()
    today = current_time.date()
    two_weeks_ago = today - timedelta(days=14)

    # Get residents who don't have a completed appointment in the last 14 days
    residents_with_recent_appointments = Appointment.objects.filter(
        status='Completed',
        appointment_date__gte=two_weeks_ago
    ).values_list('resident_id', flat=True)

    residents_with_scheduled_appointments = Appointment.objects.filter(
        status='Scheduled'
    ).values_list('resident_id', flat=True)

    residents = CustomUser.objects.filter(
        role='student'
    ).exclude(id__in=residents_with_recent_appointments).exclude(id__in=residents_with_scheduled_appointments)

    # Generate available time slots dynamically (8:00 AM - 8:00 PM, every 15 mins)
    available_time_slots = []
    start_time = time(8, 0)
    end_time = time(20, 0)
    current_slot = datetime.combine(today, start_time)

    while current_slot.time() < end_time:
        # Check if this time slot is already booked
        if not Appointment.objects.filter(
            clinic=clinic,
            appointment_date=today,
            appointment_time=current_slot.time()
        ).exists():
            available_time_slots.append(current_slot.strftime("%H:%M"))

        current_slot += timedelta(minutes=15)  # Increment time slot

    if request.method == 'POST':
        resident_id = request.POST.get('resident')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        if not resident_id or not appointment_date or not appointment_time:
            messages.error(request, "All fields are required.")
            return redirect('book_appointment')

        resident = CustomUser.objects.filter(id=resident_id, role='student').first()
        if not resident:
            messages.error(request, "Invalid resident selected.")
            return redirect('book_appointment')

        # Convert input values to datetime objects
        appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        appointment_time_obj = datetime.strptime(appointment_time, "%H:%M").time()

        # Ensure appointment is in the future
        if appointment_date < today or (appointment_date == today and appointment_time_obj <= current_time.time()):
            messages.error(request, "You cannot book an appointment in the past. Please select a future time.")
            return redirect('book_appointment')

        # Ensure appointment time is within working hours
        if appointment_time_obj < time(8, 0) or appointment_time_obj > time(20, 0):
            messages.error(request, "Appointments can only be booked between 8:00 AM and 8:00 PM.")
            return redirect('book_appointment')

        # Ensure the selected time slot is available
        if appointment_time not in available_time_slots:
            messages.error(request, "The selected time slot is not available. Please choose another time.")
            return redirect('book_appointment')

        # Generate a unique appointment ID
        last_appointment = Appointment.objects.order_by('-appointment_id').first()
        last_id_number = int(last_appointment.appointment_id[4:]) if last_appointment else 0
        appointment_id = f"APPT{last_id_number + 1:04d}"

        # Create the appointment
        Appointment.objects.create(
            appointment_id=appointment_id,
            resident=resident,
            clinic=clinic,
            appointment_date=appointment_date,
            appointment_time=appointment_time_obj,
            result="Pending",
        )

        messages.success(request, f"Appointment booked successfully for {resident.full_name} on {appointment_date} at {appointment_time_obj}.")
        return redirect('manage_appointments')

    return render(request, 'appointments/book_appointment.html', {
        'clinic': clinic,
        'today': today,
        'available_time_slots': available_time_slots,
        'residents': residents
    })

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(resident=request.user)
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)

    if request.user.role not in ['admin', 'superadmin']:
        messages.error(request, "You are not authorized to edit appointments.")
        return redirect('appointment_list')

    # Generate 15-minute time slots
    time_slots = [
        (datetime.combine(datetime.today(), time(8, 0)) + timedelta(minutes=15 * i)).time()
        for i in range(48)  # 48 slots from 8:00 AM to 8:00 PM
    ]

    # Get booked times (excluding the current appointment being edited)
    booked_times = set(
        Appointment.objects.filter(
            clinic=appointment.clinic,
            appointment_date=appointment.appointment_date
        ).exclude(id=appointment.id).values_list('appointment_time', flat=True)
    )

    # Ensure available_time_slots is actually used
    available_time_slots = [slot for slot in time_slots if slot not in booked_times]

    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        if not appointment_date or not appointment_time:
            messages.error(request, "Both date and time are required.")
            return redirect('edit_appointment', appointment_id=appointment_id)

        try:
            appointment_time_obj = datetime.strptime(appointment_time, "%H:%M").time()
        except ValueError:
            messages.error(request, "Invalid time format. Please select a valid time.")
            return redirect('edit_appointment', appointment_id=appointment_id)

        if appointment_time_obj in booked_times:
            messages.error(request, "The selected timeslot is already taken. Please choose another time.")
            return redirect('edit_appointment', appointment_id=appointment_id)

        # Update the appointment
        appointment.appointment_date = appointment_date
        appointment.appointment_time = appointment_time_obj
        appointment.save()

        messages.success(request, "Appointment updated successfully.")
        return redirect('manage_appointments')

    # Ensure the variable is actually returned
    return render(request, 'appointments/edit_appointment.html', {
        'appointment': appointment,
        'time_slots': available_time_slots  # Ensuring it's passed
    })

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)

    current_time = now()

    # Prevent residents from canceling past appointments
    if request.user == appointment.resident and appointment.appointment_date < current_time.date():
        messages.error(request, "You cannot cancel an appointment that has already passed.")
        return redirect('appointment_list')

    # Allow only admins to cancel past appointments
    if request.user.role in ['admin', 'superadmin'] or (request.user == appointment.resident and appointment.appointment_date >= current_time.date()):
        appointment.delete()
        messages.success(request, "Appointment canceled successfully.")
    else:
        messages.error(request, "You are not authorized to cancel this appointment.")
        return redirect('home')

    # Redirect based on user role
    if request.user.role in ['admin', 'superadmin']:
        return redirect('manage_appointments')  # Admin stays on manage page
    else:
        return redirect('appointment_list')  # Regular users go back to their list

@login_required
def report_health(request):
    clinic = Clinic.objects.first()

    if not clinic:
        messages.error(request, "No clinic available for appointments. Please contact admin.")
        return redirect('home')

    current_time = now()

    # Check for ongoing scheduled appointment
    ongoing_appointment = Appointment.objects.filter(
        resident=request.user,
        clinic=clinic,
        status='Scheduled'
    ).exists()

    # Check for recent appointments within the past 14 days
    fourteen_days_ago = current_time.date() - timedelta(days=14)
    recent_appointment = Appointment.objects.filter(
        resident=request.user,
        clinic=clinic,
        appointment_date__gte=fourteen_days_ago
    ).exists()

    if request.method == 'POST':
        has_symptoms = request.POST.get('has_symptoms', 'no')

        if has_symptoms == 'no':
            messages.success(request, "You are safe! Stay healthy!")
            return redirect('home')

        if ongoing_appointment:
            messages.warning(request, "You already have a scheduled appointment. Please wait until it is completed.")
            return redirect('appointment_list')

        if recent_appointment:
            messages.warning(request, "You have already had an appointment in the last 14 days. Please wait before booking another.")
            return redirect('appointment_list')

        # Determine the correct appointment date and time
        appointment_date = current_time.date()
        appointment_time = time(8, 0)  # Default to 08:00 (24-hour format)

        if current_time.time() >= time(20, 0):  
            # If it's past 20:00 (8 PM), move to the next day
            appointment_date += timedelta(days=1)
            appointment_time = time(8, 0)
        else:
            # Find the next available 15-minute slot **in 24-hour format**
            next_slot = (current_time + timedelta(minutes=15)).time()
            while next_slot.minute % 15 != 0:
                next_slot = (datetime.combine(appointment_date, next_slot) + timedelta(minutes=1)).time()

            appointment_time = next_slot if next_slot >= time(8, 0) else time(8, 0)

        # Ensure the selected slot is actually available
        while Appointment.objects.filter(
            clinic=clinic,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists():
            appointment_time = (datetime.combine(appointment_date, appointment_time) + timedelta(minutes=15)).time()
            if appointment_time >= time(20, 0):  
                # Move to the next day if the last slot is full
                appointment_date += timedelta(days=1)
                appointment_time = time(8, 0)

        # Generate a unique appointment ID
        last_appointment = Appointment.objects.order_by('-appointment_id').first()
        last_id_number = int(last_appointment.appointment_id[4:]) if last_appointment else 0
        appointment_id = f"APPT{last_id_number + 1:04d}"

        # Create the appointment
        Appointment.objects.create(
            appointment_id=appointment_id,
            resident=request.user,
            clinic=clinic,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            result="Pending",
        )

        messages.success(request, f"An appointment has been automatically booked for {appointment_date} at {appointment_time.strftime('%H:%M')} (24-hour format).")
        return redirect('appointment_list')

    return render(request, 'appointments/report_health.html', {
        'ongoing_appointment': ongoing_appointment,
        'recent_appointment': recent_appointment
    })

@login_required
def manage_appointments(request):
    if request.user.role not in ['admin', 'superadmin']:
        messages.error(request, "You are not authorized to manage appointments.")
        return redirect('home')

    all_appointments = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')
    ongoing_appointments = all_appointments.filter(status='Scheduled')

    return render(request, 'appointments/manage_appointments.html', {
        'all_appointments': all_appointments,
        'ongoing_appointments': ongoing_appointments
    })

@login_required
def update_appointment_result(request, appointment_id):
    """Allows admins to mark appointments as completed with a result."""
    if request.user.role not in ['admin', 'superadmin']:
        messages.error(request, "You are not authorized to update appointment results.")
        return redirect('manage_appointments')

    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)

    if request.method == 'POST':
        result = request.POST.get('result')
        if result not in ['Positive', 'Negative']:
            messages.error(request, "Invalid result selection.")
            return redirect('manage_appointments')

        # Update appointment result and status
        appointment.result = result
        appointment.status = 'Completed'
        appointment.save()

        # If result is positive, mark resident as infected and relocate them
        if result == 'Positive':
            appointment.resident.mark_infected(request)  # Ensure request is passed
            relocate_resident_to_quarantine(request, appointment.resident)  # ✅ Fix: Now passing `request`

        messages.success(request, f"Appointment result updated successfully: {result}.")
        return redirect('manage_appointments')

    return render(request, 'appointments/update_result.html', {'appointment': appointment})

def relocate_resident_to_quarantine(request, resident):
    """
    Relocates infected residents to an available quarantine room in an infected hostel.
    If no infected hostel is available, an admin must assign them manually.
    """
    if not resident.rooms_assigned.exists():
        messages.warning(request, f"{resident.full_name} is not a resident and will not be quarantined.")
        return

    infected_hostel = Hostel.objects.filter(is_infected_hostel=True).first()
    if not infected_hostel:
        messages.warning(request, "No infected hostel available. Please assign manually.")
        return

    available_room = Room.objects.filter(hostel=infected_hostel, resident__isnull=True).first()
    if available_room:
        # Save original room before relocating
        health_status, created = ResidentHealthStatus.objects.get_or_create(resident=resident)
        health_status.original_room = resident.rooms_assigned.first()
        health_status.infected_since = now().date()
        health_status.save()

        # Move resident to quarantine
        resident.rooms_assigned.first().resident = None  # Vacate old room
        resident.rooms_assigned.first().save()

        resident.rooms_assigned.set([available_room])  # Assign new quarantine room
        resident.infected_status = "infected"
        resident.save()

        available_room.resident = resident
        available_room.save()

        messages.success(request, f"{resident.full_name} has been relocated to quarantine in {infected_hostel.name}.")
    else:
        messages.warning(request, "No available quarantine rooms.")

def mark_recovered(request):
    """
    Automatically marks infected residents as recovered after 14 days and moves them back to their original room.
    """
    two_weeks_ago = now().date() - timedelta(days=14)

    # Get all residents with a positive test result older than 14 days
    recovered_residents = CustomUser.objects.filter(
        infected_status="infected",
        health_status__infected_since__lte=two_weeks_ago
    ).distinct()

    for resident in recovered_residents:
        health_status = resident.health_status

        if health_status.original_room and not health_status.original_room.is_occupied():
            # Move back to the original room
            original_room = health_status.original_room
            original_room.resident = resident
            original_room.save()

            # Reset resident's health status
            health_status.original_room = None
            health_status.infected_since = None
            health_status.save()

            resident.infected_status = "recovered"
            resident.save()

            messages.success(request, f"{resident.full_name} has recovered and returned to their original room.")
        else:
            messages.warning(request, f"{resident.full_name} cannot be relocated yet. Their original room is occupied.")
