from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment, Clinic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, time, timedelta

@login_required
def book_appointment(request):
    clinic = Clinic.objects.first()  # Fetch the first clinic available

    if not clinic:
        messages.error(request, "No clinic available. Please contact admin.")
        return redirect('appointment_list')

    # Check for existing pending appointments
    existing_appointment = Appointment.objects.filter(
        resident=request.user,
        clinic=clinic,
        status='Scheduled'
    ).first()

    if existing_appointment:
        messages.warning(request, "You already have a pending appointment. Please cancel it before booking a new one.")
        return redirect('appointment_list')

    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')

        if not appointment_date or not appointment_time or not reason:
            messages.error(request, "All fields are required.")
            return redirect('book_appointment')

        # Validate appointment time
        appointment_time_obj = datetime.strptime(appointment_time, "%H:%M").time()
        if appointment_time_obj < time(8, 0) or appointment_time_obj > time(20, 0):
            messages.error(request, "Appointments can only be booked between 8:00 AM and 8:00 PM.")
            return redirect('book_appointment')

        # Check for double booking
        overlapping_appointment = Appointment.objects.filter(
            clinic=clinic,
            appointment_date=appointment_date,
            appointment_time=appointment_time_obj
        ).exists()

        if overlapping_appointment:
            messages.error(request, f"The time slot at {appointment_time} is already booked. Please choose another time.")
            return redirect('book_appointment')

        # Create the appointment
        Appointment.objects.create(
            appointment_id=f"APPT{Appointment.objects.count() + 1:04d}",
            resident=request.user,
            clinic=clinic,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            result="Pending",
        )
        messages.success(request, "Appointment booked successfully.")
        return redirect('appointment_list')

    return render(request, 'appointments/book_appointment.html', {'clinic': clinic})

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

    # Allow resident to cancel their own appointment or admin to cancel any appointment
    if request.user == appointment.resident or request.user.role in ['admin', 'superadmin']:
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
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id, resident=request.user)
    appointment.confirm_appointment()
    messages.success(request, "Appointment confirmed successfully.")
    return redirect('appointment_list')

@login_required
def report_health(request):
    clinic = Clinic.objects.first()
    ongoing_appointment = Appointment.objects.filter(
        resident=request.user,
        clinic=clinic,
        status='Scheduled'
    ).first()

    if request.method == 'POST' and not ongoing_appointment:
        has_symptoms = request.POST.get('has_symptoms', 'no')

        if has_symptoms == 'no':
            messages.success(request, "You are safe! Stay healthy!")
            return redirect('home')

        if not clinic:
            messages.error(request, "No clinic available for appointments. Please contact admin.")
            return redirect('home')

        # Ensure appointment time is in the future and within clinic hours
        now = datetime.now()
        appointment_date = now.date()
        appointment_time = time(8, 0)  # Start from the clinic's opening time

        # Increment time in 15-minute slots until an available slot is found
        while Appointment.objects.filter(
            clinic=clinic,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists():
            appointment_time = (datetime.combine(appointment_date, appointment_time) + timedelta(minutes=15)).time()
            if appointment_time >= time(20, 0):  # Move to the next day if the clinic closes
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
        messages.success(request, "An appointment has been automatically booked for you.")
        return redirect('appointment_list')

    return render(request, 'appointments/report_health.html', {'ongoing_appointment': ongoing_appointment})

@login_required
def manage_appointments(request):
    if request.user.role not in ['admin', 'superadmin']:
        messages.error(request, "You are not authorized to manage appointments.")
        return redirect('home')

    all_appointments = Appointment.objects.all().order_by('appointment_date', 'appointment_time')
    ongoing_appointments = all_appointments.filter(status='Scheduled')

    return render(request, 'appointments/manage_appointments.html', {
        'all_appointments': all_appointments,
        'ongoing_appointments': ongoing_appointments
    })
