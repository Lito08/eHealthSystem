from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Hotspot
from .forms import HotspotForm

@login_required
def manage_hotspots(request):
    """Allow superadmin and admin to manage hotspots."""
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to manage hotspots.")
        return redirect('dashboard')

    hotspots = Hotspot.objects.all()
    return render(request, 'hotspots/manage_hotspots.html', {'hotspots': hotspots})

@login_required
def add_hotspot(request):
    """Allow superadmin and admin to add a new hotspot."""
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to add hotspots.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = HotspotForm(request.POST)
        if form.is_valid():
            hotspot = form.save(commit=False)

            # Check for duplicate hotspot names
            if Hotspot.objects.filter(name=hotspot.name).exists():
                messages.error(request, "A hotspot with this name already exists.")
                return render(request, 'hotspots/add_hotspot.html', {'form': form})

            # Ensure latitude and longitude are provided
            if not hotspot.latitude or not hotspot.longitude:
                messages.error(request, "Please select a location on the map before submitting.")
                return render(request, 'hotspots/add_hotspot.html', {'form': form})

            hotspot.save()
            messages.success(request, "Hotspot added successfully!")
            return redirect('manage_hotspots')
    else:
        form = HotspotForm()

    return render(request, 'hotspots/add_hotspot.html', {'form': form})

@login_required
def edit_hotspot(request, hotspot_id):
    """Allow superadmin and admin to edit an existing hotspot."""
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to edit hotspots.")
        return redirect('dashboard')

    hotspot = get_object_or_404(Hotspot, id=hotspot_id)

    if request.method == 'POST':
        form = HotspotForm(request.POST, instance=hotspot)
        if form.is_valid():
            updated_hotspot = form.save(commit=False)

            # Check for duplicate hotspot names (excluding the current one)
            if Hotspot.objects.exclude(id=hotspot_id).filter(name=updated_hotspot.name).exists():
                messages.error(request, "A hotspot with this name already exists.")
                return render(request, 'hotspots/edit_hotspot.html', {'form': form, 'hotspot': hotspot})

            # Ensure latitude and longitude are provided
            if not updated_hotspot.latitude or not updated_hotspot.longitude:
                messages.error(request, "Please select a location on the map before submitting.")
                return render(request, 'hotspots/edit_hotspot.html', {'form': form, 'hotspot': hotspot})

            updated_hotspot.save()
            messages.success(request, "Hotspot updated successfully!")
            return redirect('manage_hotspots')
    else:
        form = HotspotForm(instance=hotspot)

    return render(request, 'hotspots/edit_hotspot.html', {'form': form, 'hotspot': hotspot})

@login_required
def delete_hotspot(request, hotspot_id):
    """Allow superadmin and admin to delete hotspots."""
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to delete hotspots.")
        return redirect('dashboard')

    hotspot = get_object_or_404(Hotspot, id=hotspot_id)
    hotspot.delete()
    messages.success(request, "Hotspot deleted successfully!")
    return redirect('manage_hotspots')

@login_required
def view_hotspots(request):
    """Allow residents to view the list of hotspots."""
    hotspots = Hotspot.objects.all()
    return render(request, 'hotspots/view_hotspots.html', {'hotspots': hotspots})

@login_required
def get_hotspots(request):
    """ Return hotspot data as JSON for the heatmap. """
    hotspots = Hotspot.objects.values('name', 'latitude', 'longitude', 'infected_count', 'recovered_count')
    return JsonResponse({'hotspots': list(hotspots)})

@login_required
def heatmap_view(request):
    """Render the heatmap page for viewing COVID-19 hotspots."""
    return render(request, 'hotspots/heatmap.html')
