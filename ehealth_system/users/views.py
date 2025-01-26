from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UserRegistrationForm

CustomUser = get_user_model()

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def create_user(request):
    if request.user.role != 'superadmin':  # Ensure only superadmins can create users
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
    if request.user.role != 'superadmin':  
        messages.error(request, "You are not authorized to view users.")
        return redirect('dashboard')

    users = CustomUser.objects.exclude(role='superadmin')  # Hide other superadmins
    return render(request, 'users/user_list.html', {'users': users})
