from django.shortcuts import render, redirect, get_object_or_404
from .models import Resident, HealthStatus, QuarantineRoom
from .forms import ResidentForm, HealthStatusForm
from datetime import timedelta
from django.utils import timezone

def symptom_reporting(request):
    if request.method == 'POST':
        resident_form = ResidentForm(request.POST)
        health_form = HealthStatusForm(request.POST)
        if resident_form.is_valid() and health_form.is_valid():
            resident = resident_form.save()
            health_status = health_form.save(commit=False)
            health_status.resident = resident
            health_status.save()
            
            if health_status.status == 'Infected':
                room_number = f"Room{QuarantineRoom.objects.count() + 1}"
                start_date = timezone.now().date()
                end_date = start_date + timedelta(days=14)
                QuarantineRoom.objects.create(
                    room_number=room_number,
                    resident=resident,
                    start_date=start_date,
                    end_date=end_date
                )
            
            return redirect('health_status')
    else:
        resident_form = ResidentForm()
        health_form = HealthStatusForm()
        
        symptoms_list = [
            "Fever or chills",
            "Cough",
            "Shortness of breath or difficulty breathing",
            "Sore throat",
            "Congestion or runny nose",
            "New loss of taste or smell",
            "Fatigue",
            "Muscle or body aches",
            "Headache",
            "Nausea or vomiting",
            "Diarrhea",
        ]
        
    return render(request, 'symptom_reporting.html', {
        'resident_form': resident_form, 
        'health_form': health_form,
        'symptoms_list': symptoms_list,
    })

def health_status(request):
    statuses = HealthStatus.objects.all()
    return render(request, 'health_status.html', {'statuses': statuses})

def quarantine_management(request):
    rooms = QuarantineRoom.objects.all()
    return render(request, 'quarantine_management.html', {'rooms': rooms})

def edit_resident(request, resident_id):
    resident = get_object_or_404(Resident, id=resident_id)
    health_status = HealthStatus.objects.get(resident=resident)

    if request.method == 'POST':
        resident_form = ResidentForm(request.POST, instance=resident)
        health_form = HealthStatusForm(request.POST, instance=health_status)
        if resident_form.is_valid() and health_form.is_valid():
            resident_form.save()
            health_form.save()
            return redirect('health_status')
    else:
        resident_form = ResidentForm(instance=resident)
        health_form = HealthStatusForm(instance=health_status)

    return render(request, 'edit_resident.html', {
        'form': resident_form,
        'health_form': health_form,
    })

def delete_resident(request, resident_id):
    resident = get_object_or_404(Resident, id=resident_id)
    
    # Delete associated HealthStatus and QuarantineRoom records
    HealthStatus.objects.filter(resident=resident).delete()
    QuarantineRoom.objects.filter(resident=resident).delete()
    
    # Delete the resident
    resident.delete()
    
    return redirect('health_status')
# Create your views here.
