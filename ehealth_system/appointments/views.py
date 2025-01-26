from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment, Clinic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string

@login_required
def book_appointment(request):
    clinic = Clinic.objects.first()  # Fetch the first clinic available

    if not clinic:
        messages.error(request, "No clinic available. Please contact admin.")
        return redirect('appointment_list')

    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')

        if not appointment_date or not appointment_time or not reason:
            messages.error(request, "All fields are required.")
            return redirect('book_appointment')

        Appointment.objects.create(
            appointment_id="APPT" + str(Appointment.objects.count() + 1),
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
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id, resident=request.user)
    if request.method == 'POST':
        appointment.appointment_date = request.POST['appointment_date']
        appointment.appointment_time = request.POST['appointment_time']
        appointment.reason = request.POST['reason']
        appointment.save()
        messages.success(request, "Appointment updated successfully.")
        return redirect('appointment_list')

    return render(request, 'appointments/edit_appointment.html', {'appointment': appointment})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id, resident=request.user)
    appointment.delete()
    messages.success(request, "Appointment canceled successfully.")
    return redirect('appointment_list')

@login_required
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id, resident=request.user)
    appointment.confirm_appointment()
    messages.success(request, "Appointment confirmed successfully.")
    return redirect('appointment_list')
