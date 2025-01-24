from django.shortcuts import render, redirect
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
