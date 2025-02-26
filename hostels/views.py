from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hostel, Room
from .forms import HostelForm, RoomForm

# Hostel Management
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
            messages.error(request, "Failed to add hostel. Please correct the errors.")
    else:
        form = HostelForm()

    return render(request, 'hostels/add_hostel.html', {'form': form})

@login_required
def edit_hostel(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)

    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to edit this hostel.")
        return redirect('hostel_list')

    if request.method == 'POST':
        form = HostelForm(request.POST, instance=hostel)
        if form.is_valid():
            form.save()
            messages.success(request, f"Hostel '{hostel.name}' updated successfully!")
            return redirect('hostel_list')
        else:
            messages.error(request, "Failed to update hostel. Please check for duplicate name and block.")

    else:
        form = HostelForm(instance=hostel)

    return render(request, 'hostels/edit_hostel.html', {'form': form, 'hostel': hostel})

@login_required
def delete_hostel(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to delete this hostel.")
        return redirect('hostel_list')

    hostel.delete()
    messages.success(request, f"Hostel '{hostel.name}' deleted successfully!")
    return redirect('hostel_list')

# Room Management
@login_required
def room_list(request, hostel_id):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('home')

    hostel = get_object_or_404(Hostel, id=hostel_id)
    rooms = hostel.rooms.all()
    return render(request, 'hostels/room_list.html', {'hostel': hostel, 'rooms': rooms})

@login_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to edit this room.")
        return redirect('hostel_list')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            new_resident = form.cleaned_data.get('resident')
            clear_resident = form.cleaned_data.get('clear_resident')

            # Clear existing resident assignment properly
            if clear_resident and room.resident:
                # Remove the resident from their assigned room
                previous_resident = room.resident
                previous_resident.rooms_assigned.clear()  # Remove previous room association
                previous_resident.save()

                room.resident = None  # Remove resident from the room itself
                room.save()
                messages.success(request, f"Resident cleared from Room '{room.number}'.")

            else:
                # Ensure that if a resident is moved, they are removed from their old room
                if new_resident:
                    previous_room = Room.objects.filter(resident=new_resident).first()
                    if previous_room and previous_room.id != room.id:
                        previous_room.resident = None
                        previous_room.save()

                    # Assign the resident to the new room
                    room.resident = new_resident
                    room.save()
                    messages.success(request, f"Room '{room.number}' updated successfully!")

            return redirect('room_list', hostel_id=room.hostel.id)

    else:
        form = RoomForm(instance=room)

    return render(request, 'hostels/edit_room.html', {'form': form, 'room': room})

@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to delete this room.")
        return redirect('hostel_list')

    room.delete()
    messages.success(request, f"Room '{room.number}' deleted successfully!")
    return redirect('room_list', hostel_id=room.hostel.id)
