from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm
from django.http import JsonResponse
from hostels.models import Room
from .models import CustomUser
from datetime import datetime

CustomUser = get_user_model()

def user_login(request):
    if request.method == 'POST':
        matric_id = request.POST['matric_id']
        password = request.POST['password']
        user = authenticate(request, matric_id=matric_id, password=password)
        if user is not None:
            login(request, user)
            if user.role in ['superadmin', 'admin']:
                return redirect('dashboard')  # Admins go to dashboard
            else:
                return redirect('home')  # Residents go to home
        else:
            messages.error(request, "Invalid Matric ID or password.")
    return render(request, 'users/login.html')

@login_required
def view_profile(request):
    """Allows authenticated users to view their profile details."""
    return render(request, 'users/view_profile.html', {'user': request.user})

@login_required
def dashboard(request):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    return render(request, 'dashboard.html')

@login_required
def manage_users(request):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to manage users.")
        return redirect('dashboard')

    role_filter = request.GET.get('role', 'all')

    # Superadmin can see all users including admins
    if request.user.role == 'superadmin':
        users = CustomUser.objects.exclude(role='superadmin') if role_filter == 'all' else CustomUser.objects.filter(role=role_filter)
    
    # Admin cannot see superadmins or other admins
    else:  # This means the logged-in user is an admin
        if role_filter == 'all':
            users = CustomUser.objects.exclude(role__in=['superadmin', 'admin'])
        else:
            users = CustomUser.objects.filter(role=role_filter).exclude(role='admin')

    for user in users:
        room = Room.objects.filter(resident=user).first()
        user.room_details = f"{room.hostel.block}, Room {room.number}" if room else "No room assigned"

    return render(request, 'users/manage_users.html', {'users': users, 'role_filter': role_filter})

@login_required
def create_user(request):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to create users.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user first without committing
            user = form.save(commit=False)
            user.save()  # Save the user instance to the database

            # Handle the room assignment
            room_id = request.POST.get('room')
            if room_id:
                room = Room.objects.get(id=room_id)
                room.resident = user  # Assign the user to the room
                room.save()  # Save the room instance

            messages.success(request, "User created successfully!")
            return redirect('manage_users')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/create_user.html', {'form': form})

def generate_matric_id(request):
    role = request.GET.get('role', 'student')
    year = datetime.now().year % 100

    prefix_mapping = {'admin': 'A', 'staff': 'UC', 'lecturer': 'L', 'student': 'S'}
    prefix = prefix_mapping.get(role, 'S')

    last_user = CustomUser.objects.filter(role=role).order_by('-matric_id').first()
    last_number = int(last_user.matric_id[3:]) + 1 if last_user and last_user.matric_id else 1

    matric_id = f"{year}{last_number:04d}"
    return JsonResponse({'matric_id': matric_id})

@login_required
def update_user(request, user_id):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to update user details.")
        return redirect('dashboard')

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        form.fields.pop("role", None)
        if form.is_valid():
            user = form.save(commit=False)

            # Handle room assignment
            room_id = request.POST.get('room')
            if room_id:
                try:
                    room = Room.objects.get(id=room_id)

                    # Reassign the room only if it's not already assigned to this user
                    if room.resident != user:
                        # Clear any previously assigned room
                        previous_room = Room.objects.filter(resident=user).first()
                        if previous_room:
                            previous_room.resident = None
                            previous_room.save()

                        # Assign the new room
                        room.resident = user
                        room.save()
                except Room.DoesNotExist:
                    messages.error(request, "Selected room does not exist.")
                    return redirect('update_user', user_id=user.id)
            else:
                # If no room selected, clear the previous room assignment
                previous_room = Room.objects.filter(resident=user).first()
                if previous_room:
                    previous_room.resident = None
                    previous_room.save()

            # Save the user instance
            user.save()
            messages.success(request, "User updated successfully!")
            return redirect('manage_users')
    else:
        form = UserUpdateForm(instance=user)

        # Dynamically populate room queryset
        if user.rooms_assigned.exists():
            assigned_room = user.rooms_assigned.first()
            form.fields['room'].queryset = Room.objects.filter(hostel=assigned_room.hostel).exclude(resident__isnull=False) | Room.objects.filter(id=assigned_room.id)
        else:
            form.fields['room'].queryset = Room.objects.filter(resident=None)

    return render(request, 'users/update_user.html', {'form': form, 'user': user})

@login_required
def clear_room(request, user_id):
    if request.user.role not in ['superadmin', 'admin']:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    user = get_object_or_404(CustomUser, id=user_id)
    room = Room.objects.filter(resident=user).first()
    if room:
        room.resident = None
        room.save()
    return JsonResponse({'message': 'Room cleared successfully'})

@login_required
def delete_user(request, user_id):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to delete users.")
        return redirect('dashboard')

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role == 'superadmin':
        messages.error(request, "Superadmins cannot be deleted.")
        return redirect('manage_users')

    room = Room.objects.filter(resident=user).first()
    if room:
        room.resident = None
        room.save()

    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('manage_users')

@login_required
def get_rooms(request):
    hostel_id = request.GET.get('hostel_id')
    user_id = request.GET.get('user_id')  # Pass the current user ID for editing

    if hostel_id:
        # Fetch rooms for the selected hostel
        rooms = Room.objects.filter(hostel_id=hostel_id, resident=None).values('id', 'number')

        # Include the assigned room for the user if editing
        if user_id:
            user = CustomUser.objects.get(id=user_id)
            assigned_room = Room.objects.filter(resident=user).first()
            if assigned_room and assigned_room.hostel.id == int(hostel_id):
                rooms = rooms.union(Room.objects.filter(id=assigned_room.id).values('id', 'number'))

        return JsonResponse({'rooms': list(rooms)})
    return JsonResponse({'rooms': []})
