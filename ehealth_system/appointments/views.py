from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment, Clinic
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def book_appointment(request):
    if request.method == 'POST':
        clinic_id = request.POST['clinic']
        appointment_date = request.POST['appointment_date']
        reason = request.POST['reason']

        clinic = Clinic.objects.get(id=clinic_id)
        Appointment.objects.create(
            resident=request.user,
            clinic=clinic,
            appointment_date=appointment_date,
            reason=reason
        )
        messages.success(request, "Appointment booked successfully.")
        return redirect('appointment_list')

    clinics = Clinic.objects.all()
    return render(request, 'appointments/book_appointment.html', {'clinics': clinics})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(resident=request.user)
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, resident=request.user)
    if request.method == 'POST':
        appointment.appointment_date = request.POST['appointment_date']
        appointment.reason = request.POST['reason']
        appointment.save()
        messages.success(request, "Appointment updated successfully.")
        return redirect('appointment_list')

    return render(request, 'appointments/edit_appointment.html', {'appointment': appointment})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, resident=request.user)
    appointment.delete()
    messages.success(request, "Appointment canceled successfully.")
    return redirect('appointment_list')
