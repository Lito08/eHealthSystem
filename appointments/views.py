import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Appointment, Clinic
from users.models import CustomUser
from hostels.models import Hostel, Room, ResidentHealthStatus
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, time, timedelta
from django.utils.timezone import localtime, now

### HELPERS ###
def generate_time_slots():
    """Generates 15-minute interval time slots from 08:00 to 20:00."""
    return [
        (datetime.combine(datetime.today(), time(8, 0)) + timedelta(minutes=15 * i)).strftime("%H:%M")
        for i in range(48)  # 48 slots from 8:00 AM to 8:00 PM
    ]

def get_booked_slots(appointment_date):
    """Fetches already booked time slots for a given date."""
    return set(
        Appointment.objects.filter(appointment_date=appointment_date)
        .values_list('appointment_time', flat=True)
    )

def get_available_time_slots(appointment_date):
    """Filters out booked slots from the generated time slots."""
    booked_times = get_booked_slots(appointment_date)
    return [slot for slot in generate_time_slots() if slot not in booked_times]

### AJAX ENDPOINT ###
@login_required
def get_available_slots(request):
    """Fetch available time slots for booking and editing an appointment."""
    resident_id = request.GET.get('resident_id')
    appointment_date = request.GET.get('appointment_date')
    appointment_id = request.GET.get('appointment_id', None)  # Get appointment ID if provided

    if not resident_id or not appointment_date:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    try:
        resident = CustomUser.objects.get(id=resident_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "Resident not found"}, status=404)

    local_now = localtime(now())  # Ensure correct local time
    today = local_now.date()
    current_time = local_now.time()

    try:
        appointment_date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Invalid date format"}, status=400)

    # ✅ Prevent booking/editing today if it's past 8 PM
    if appointment_date_obj == today and current_time >= time(20, 0):
        return JsonResponse({"error": "Appointments cannot be booked after 8 PM today."}, status=403)

    # ✅ Fetch booked slots, excluding the current appointment if editing
    booked_slots = set(
        Appointment.objects.filter(
            appointment_date=appointment_date_obj
        ).exclude(appointment_id=appointment_id)
        .values_list('appointment_time', flat=True)
    )

    # ✅ Generate all 15-minute slots from 8 AM to 8 PM
    all_time_slots = [
        (datetime.combine(today, time(8, 0)) + timedelta(minutes=15 * i)).strftime("%H:%M")
        for i in range(48)  # 48 slots from 8:00 AM to 8:00 PM
    ]

    # ✅ Remove booked slots and prevent selecting past time for today
    available_time_slots = [
        slot for slot in all_time_slots
        if slot not in booked_slots and (appointment_date_obj > today or slot >= current_time.strftime("%H:%M"))
    ]

    return JsonResponse({"available_time_slots": available_time_slots})

### APPOINTMENT BOOKING ###
@login_required
def book_appointment(request):
    """Handles booking an appointment for a resident."""
    clinic = Clinic.objects.first()
    if not clinic:
        messages.error(request, "No clinic available. Please contact admin.")
        return redirect('manage_appointments')

    today = now().date()
    fourteen_days_ago = today - timedelta(days=14)

    # ✅ **Filter residents who haven't had an appointment in the last 14 days**
    # ✅ **Exclude admins and superadmins from selection**
    residents = CustomUser.objects.exclude(
        role__in=['admin', 'superadmin']
    ).exclude(
        id__in=Appointment.objects.filter(
            appointment_date__gte=fourteen_days_ago
        ).values_list('resident_id', flat=True)
    ).distinct()

    available_time_slots = generate_time_slots()

    if request.method == 'POST':
        resident_id = request.POST.get('resident')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        if not resident_id or not appointment_date or not appointment_time:
            messages.error(request, "All fields are required.")
            return redirect('book_appointment')

        resident = get_object_or_404(CustomUser, id=resident_id)

        # ✅ Ensure only valid residents can book
        if resident.role in ['admin', 'superadmin']:
            messages.error(request, "Admins are not allowed to book appointments.")
            return redirect('book_appointment')

        appointment_date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()

        # ✅ **Check if the selected time is actually available**
        if appointment_time not in get_available_time_slots(appointment_date_obj):
            messages.error(request, "The selected time slot is not available. Please choose another time.")
            return redirect('book_appointment')

        # ✅ **Check if another appointment already exists at the same time**
        if Appointment.objects.filter(appointment_date=appointment_date, appointment_time=appointment_time, clinic=clinic).exists():
            messages.error(request, "This time slot is already booked by another resident. Please choose another time.")
            return redirect('book_appointment')

        # ✅ **Create the appointment**
        Appointment.objects.create(
            resident=resident,
            clinic=clinic,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            result="Pending",
        )

        messages.success(request, f"Appointment for {resident.full_name} booked successfully.")
        return redirect('manage_appointments')

    return render(request, 'appointments/book_appointment.html', {
        'clinic': clinic,
        'residents': residents,
        'available_time_slots': available_time_slots,
        'today': today
    })

### REPORT HEALTH ###
@login_required
def report_health(request):
    """Handles self-reporting of health risk and automatic appointment booking."""
    clinic = Clinic.objects.first()
    if not clinic:
        messages.error(request, "No clinic available for appointments. Please contact admin.")
        return redirect('home')

    # ✅ Get correct timezone-aware local date
    today = localtime(now()).date()
    fourteen_days_ago = today - timedelta(days=14)

    # ✅ Check for recent active appointments within the past 14 days
    recent_appointment = Appointment.objects.filter(
        resident=request.user, 
        appointment_date__gte=fourteen_days_ago,
        status__in=['Scheduled', 'Pending', 'Confirmed']
    ).exists()

    if request.method == 'POST':
        has_symptoms = request.POST.get('has_symptoms', 'no')

        if has_symptoms == 'no':
            messages.success(request, "You are safe! Stay healthy!")
            return redirect('home')

        if recent_appointment:
            messages.warning(request, "You already have an active appointment within the last 14 days.")
            return redirect('appointment_list')

        # ✅ Get next available slot for today
        available_time_slots = get_available_time_slots(today)

        if not available_time_slots:
            messages.error(request, "No available time slots today. Please try tomorrow.")
            return redirect('appointment_list')

        appointment_time = available_time_slots[0]  # ✅ Pick the first available slot

        # ✅ Ensure the slot is actually available before booking
        if Appointment.objects.filter(appointment_date=today, appointment_time=appointment_time, clinic=clinic).exists():
            messages.error(request, "This time slot is no longer available. Please try another time.")
            return redirect('appointment_list')

        # ✅ Create an appointment
        Appointment.objects.create(
            resident=request.user,
            clinic=clinic,
            appointment_date=today,
            appointment_time=appointment_time,
            result="Pending",
        )

        messages.success(request, f"An appointment has been booked for {today} at {appointment_time}.")
        return redirect('appointment_list')

    return render(request, 'appointments/report_health.html', {
        'recent_appointment': recent_appointment
    })

### APPOINTMENT MANAGEMENT ###
@login_required
def manage_appointments(request):
    """Allows admins to manage and view all appointments."""
    if request.user.role not in ['admin', 'superadmin']:
        messages.error(request, "You are not authorized to manage appointments.")
        return redirect('home')

    # ✅ Ensure correct timezone-aware date
    today = localtime(now()).date()

    # ✅ Fetch all appointments, sorting them by date & time
    all_appointments = Appointment.objects.all().order_by('appointment_date', 'appointment_time')

    # ✅ Filter only ongoing (Scheduled & Pending) appointments for active management
    ongoing_appointments = all_appointments.filter(status__in=['Scheduled', 'Pending'])

    return render(request, 'appointments/manage_appointments.html', {
        'all_appointments': all_appointments,
        'ongoing_appointments': ongoing_appointments,
        'today': today
    })

@login_required
def appointment_list(request):
    """Displays all appointments for the logged-in resident."""
    appointments = Appointment.objects.filter(resident=request.user)
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def edit_appointment(request, appointment_id):
    """Allows admins to edit an existing appointment's date and time."""
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)

    if request.user.role not in ['admin', 'superadmin']:
        messages.error(request, "You are not authorized to edit appointments.")
        return redirect('appointment_list')

    clinic = appointment.clinic
    today = localtime(now()).date()
    current_time = localtime(now()).time()

    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        if not appointment_date or not appointment_time:
            messages.error(request, "Both date and time are required.")
            return redirect('edit_appointment', appointment_id=appointment_id)

        try:
            appointment_date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('edit_appointment', appointment_id=appointment_id)

        # ✅ **Ensure no past time slots are selected for today**
        if appointment_date_obj == today and appointment_time < current_time.strftime("%H:%M"):
            messages.error(request, "You cannot select a past time slot for today.")
            return redirect('edit_appointment', appointment_id=appointment_id)

        # ✅ **Check if the selected time slot is actually available**
        booked_slots = set(
            Appointment.objects.filter(appointment_date=appointment_date_obj, clinic=clinic)
            .exclude(appointment_id=appointment_id)
            .values_list('appointment_time', flat=True)
        )

        if appointment_time in booked_slots:
            messages.error(request, "The selected time slot is already booked. Please choose another time.")
            return redirect('edit_appointment', appointment_id=appointment_id)

        # ✅ **Update appointment**
        appointment.appointment_date = appointment_date_obj
        appointment.appointment_time = appointment_time
        appointment.save()

        messages.success(request, "Appointment updated successfully.")
        return redirect('manage_appointments')

    # ✅ **Get available time slots excluding fully booked ones**
    booked_slots = set(
        Appointment.objects.filter(appointment_date=appointment.appointment_date, clinic=clinic)
        .exclude(appointment_id=appointment_id)
        .values_list('appointment_time', flat=True)
    )

    all_time_slots = [
        (datetime.combine(today, time(8, 0)) + timedelta(minutes=15 * i)).strftime("%H:%M")
        for i in range(48)  # Slots from 8 AM to 8 PM
    ]

    available_time_slots = [slot for slot in all_time_slots if slot not in booked_slots]

    return render(request, 'appointments/edit_appointment.html', {
        'appointment': appointment,
        'available_time_slots': available_time_slots,
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

        # **From Positive → Negative: Move Back to Original Room or Find a New One**
        elif previous_result == 'Positive' and result == 'Negative':
            relocate_back_to_original_room(request, resident)

        messages.success(request, "Appointment result updated successfully.")
        return redirect('manage_appointments')

    return render(request, 'appointments/update_result.html', {'appointment': appointment})

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
            # **Find an available room if original is occupied**
            available_room = Room.objects.filter(resident__isnull=True).first()

            if available_room:
                # Free the quarantine room
                if resident.room:
                    resident.room.resident = None
                    resident.room.save()

                resident.room = available_room
                resident.infected_status = "healthy"
                resident.save()

                available_room.resident = resident
                available_room.save()

                messages.success(request, f"{resident.full_name} has recovered but was moved to an available room.")
            else:
                messages.warning(request, f"{resident.full_name}'s original room is occupied! No available rooms.")
    else:
        messages.warning(request, f"{resident.full_name} has no original room on record.")

@login_required
def cancel_appointment(request, appointment_id):
    """Allows residents and admins to cancel an appointment."""
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)

    if request.user != appointment.resident and request.user.role not in ['admin', 'superadmin']:
        messages.error(request, "You are not authorized to cancel this appointment.")
        return redirect('home')

    appointment.delete()
    messages.success(request, "Appointment canceled successfully.")

    return redirect('manage_appointments' if request.user.role in ['admin', 'superadmin'] else 'appointment_list')
