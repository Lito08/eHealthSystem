from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hotspot
from .forms import HotspotForm

@login_required
def manage_hotspots(request):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to manage hotspots.")
        return redirect('dashboard')

    hotspots = Hotspot.objects.all()

    return render(request, 'hotspots/manage_hotspots.html', {'hotspots': hotspots})

@login_required
def add_hotspot(request):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to add hotspots.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = HotspotForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotspot added successfully!")
            return redirect('manage_hotspots')
    else:
        form = HotspotForm()

    return render(request, 'hotspots/add_hotspot.html', {'form': form})

@login_required
def edit_hotspot(request, hotspot_id):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to edit hotspots.")
        return redirect('dashboard')

    hotspot = get_object_or_404(Hotspot, id=hotspot_id)
    
    if request.method == 'POST':
        form = HotspotForm(request.POST, instance=hotspot)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotspot updated successfully!")
            return redirect('manage_hotspots')
    else:
        form = HotspotForm(instance=hotspot)

    return render(request, 'hotspots/edit_hotspot.html', {'form': form, 'hotspot': hotspot})

@login_required
def delete_hotspot(request, hotspot_id):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to delete hotspots.")
        return redirect('dashboard')

    hotspot = get_object_or_404(Hotspot, id=hotspot_id)
    hotspot.delete()
    messages.success(request, "Hotspot deleted successfully!")
    return redirect('manage_hotspots')

@login_required
def view_hotspots(request):
    hotspots = Hotspot.objects.all()

    return render(request, 'hotspots/view_hotspots.html', {'hotspots': hotspots})
