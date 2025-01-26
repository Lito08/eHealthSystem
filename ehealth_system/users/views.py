from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UserRegistrationForm
from django.http import JsonResponse
from hostels.models import Room

CustomUser = get_user_model()

@login_required
def dashboard(request):
    # Ensure only superadmins and admins can access
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    
    return render(request, 'dashboard.html')

@login_required
def create_user(request):
    print(f"User role: {request.user.role}")  # Debugging print to verify role in terminal

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
