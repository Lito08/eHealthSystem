from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hostel, Room
from .forms import HostelForm

@login_required
def hostel_list(request):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('home')
    hostels = Hostel.objects.all()
    return render(request, 'hostels/hostel_list.html', {'hostels': hostels})

@login_required
def add_hostel(request):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('hostel_list')

    if request.method == 'POST':
        form = HostelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hostel added successfully!")
            return redirect('hostel_list')
    else:
        form = HostelForm()

    return render(request, 'hostels/add_hostel.html', {'form': form})

@login_required
def room_list(request, hostel_id):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('home')

    hostel = get_object_or_404(Hostel, id=hostel_id)
    rooms = hostel.rooms.all()
    return render(request, 'hostels/room_list.html', {'hostel': hostel, 'rooms': rooms})
