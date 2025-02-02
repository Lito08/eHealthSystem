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
    clinic = Clinic.objects.first()  # Fetch the first available clinic

    if not clinic:
        messages.error(request, "No clinic available. Please contact admin.")
        return redirect('manage_appointments')  # ✅ Redirect to manage_appointments

    if request.method == 'POST':
        resident_id = request.POST.get('resident')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        if not resident_id or not appointment_date or not appointment_time:
            messages.error(request, "All fields are required.")
            return redirect('book_appointment')

        resident = get_object_or_404(CustomUser, id=resident_id)

        # Create the appointment
        Appointment.objects.create(
            resident=resident,
            clinic=clinic,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            result="Pending",
        )

        messages.success(request, f"Appointment for {resident.full_name} booked successfully.")
        return redirect('manage_appointments')  # ✅ Redirect to `manage_appointments` to show messages

    residents = CustomUser.objects.filter(role='student')  # Example: Filter residents
    return render(request, 'appointments/book_appointment.html', {'clinic': clinic, 'residents': residents})

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

    all_appointments = Appointment.objects.all().order_by('appointment_date', 'appointment_time')
    ongoing_appointments = all_appointments.filter(status='Scheduled')

    return render(request, 'appointments/manage_appointments.html', {
        'all_appointments': all_appointments,
        'ongoing_appointments': ongoing_appointments,
        'today': now().date()  # ✅ Pass today as context
    })

@login_required
def update_appointment_result(request, appointment_id):
    """Allows admins to mark appointments as completed with a result."""
    if request.user.role not in ['admin', 'superadmin']:
        messages.error(request, "You are not authorized to update appointment results.")
        return redirect('manage_appointments')

    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    previous_result = appointment.result  # Store previous result before update

    if request.method == 'POST':
        result = request.POST.get('result')
        if result not in ['Positive', 'Negative']:
            messages.error(request, "Invalid result selection.")
            return redirect('manage_appointments')

        appointment.result = result
        appointment.status = 'Completed'
        appointment.save()

        resident = appointment.resident

        # **From Pending/Negative → Positive: Move to Quarantine**
        if previous_result in ['Pending', 'Negative'] and result == 'Positive':
            if hasattr(resident, 'mark_infected'):
                resident.mark_infected(request)  # Move to quarantine
            else:
                messages.warning(request, f"{resident.full_name} does not have an `infected_status` attribute.")

        # **From Positive → Negative: Move Back to Original Room**
        elif previous_result == 'Positive' and result == 'Negative':
            relocate_back_to_original_room(request, resident)

        messages.success(request, "Appointment result updated successfully.")
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

def recover_resident_from_quarantine(request, resident):
    """Moves a recovered resident back to their original room or assigns a new room if occupied."""
    if resident.infected_status != "infected":
        messages.warning(request, f"{resident.full_name} is not in quarantine.")
        return

    health_status = resident.health_status

    # **If the original room is available, move them back**
    if health_status.original_room and not health_status.original_room.is_occupied:
        resident.room.resident = None  # Free the quarantine room
        resident.room.save()

        resident.room = health_status.original_room
        resident.infected_status = "healthy"
        resident.save()

        health_status.original_room.resident = resident
        health_status.original_room.save()
        health_status.original_room = None  # Reset stored room
        health_status.save()

        messages.success(request, f"{resident.full_name} has recovered and returned to their original room.")

    else:
        # **If the original room is occupied, find an available normal room**
        available_room = Room.find_available_normal_room()

        if available_room:
            resident.room.resident = None  # Free quarantine room
            resident.room.save()

            resident.room = available_room
            resident.infected_status = "healthy"
            resident.save()

            available_room.resident = resident
            available_room.save()

            messages.success(request, f"{resident.full_name} has recovered but was moved to an available room.")
        else:
            messages.warning(request, f"{resident.full_name} has recovered but no available rooms.")

def relocate_back_to_original_room(request, resident):
    """Moves a recovered resident back to their original room safely."""

    if resident.infected_status != "infected":
        messages.warning(request, f"{resident.full_name} is not in quarantine.")
        return

    # **Ensure the resident has a health status record**
    health_status, created = ResidentHealthStatus.objects.get_or_create(resident=resident)

    if health_status.original_room:
        original_room = health_status.original_room

        # Check if the original room is available
        if original_room.resident is None:
            # Free the quarantine room
            if resident.room:
                resident.room.resident = None
                resident.room.save()

            # Move resident back to their original room
            resident.room = original_room
            resident.infected_status = "healthy"
            resident.save()

            original_room.resident = resident
            original_room.save()

            # Reset the stored original room data
            health_status.original_room = None
            health_status.infected_since = None
            health_status.save()

            messages.success(request, f"{resident.full_name} has recovered and returned to their original room.")
        else:
            messages.warning(request, f"{resident.full_name}'s original room is occupied! Manual admin intervention is required.")
    else:
        messages.warning(request, f"{resident.full_name} has no original room on record.")


