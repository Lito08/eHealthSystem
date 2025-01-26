from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UserRegistrationForm
from django.http import JsonResponse
from hostels.models import Room
from .models import CustomUser
from datetime import datetime

CustomUser = get_user_model()

@login_required
def dashboard(request):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    return render(request, 'dashboard.html')

@login_required
def create_user(request):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to create users.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('user_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/create_user.html', {'form': form})

def generate_matric_id(request):
    role = request.GET.get('role', 'student')
    year = datetime.now().year % 100  # Get last two digits of the current year

    prefix_mapping = {
        'admin': 'A',
        'staff': 'UC',
        'lecturer': 'L',
        'student': 'S'
    }
    prefix = prefix_mapping.get(role, 'S')

    last_user = CustomUser.objects.filter(role=role).order_by('-matric_id').first()
    if last_user and last_user.matric_id:
        last_number = int(last_user.matric_id[3:]) + 1
    else:
        last_number = 1

    matric_id = f"{year}{last_number:04d}"
    return JsonResponse({'matric_id': matric_id})

@login_required
def user_list(request):
    if request.user.role not in ['superadmin', 'admin']:  
        messages.error(request, "You are not authorized to view users.")
        return redirect('dashboard')

    users = CustomUser.objects.exclude(role='superadmin')  # Hide other superadmins
    return render(request, 'users/user_list.html', {'users': users})

@login_required
def get_rooms(request):
    hostel_id = request.GET.get('hostel_id')
    if hostel_id:
        rooms = Room.objects.filter(hostel_id=hostel_id).values('id', 'number')
        return JsonResponse({'rooms': list(rooms)})
    return JsonResponse({'rooms': []})

@login_required
def update_user(request, user_id):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to update user details.")
        return redirect('dashboard')

    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect('user_list')
    else:
        form = UserRegistrationForm(instance=user)
    
    return render(request, 'users/update_user.html', {'form': form, 'user': user})

def user_login(request):
    if request.method == 'POST':
        matric_id = request.POST['matric_id']
        password = request.POST['password']
        user = authenticate(request, matric_id=matric_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Matric ID or password.")
    return render(request, 'users/login.html')
