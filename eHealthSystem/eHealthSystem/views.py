from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import ResidentForm
from .models import Resident, User, Room, Block, Level
from django.contrib.auth import authenticate, login, logout
import random
import string
from django.http import JsonResponse

# Function to generate a random password (if needed)
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

@login_required
def create_resident(request):
    # Only superusers (admins) can create residents
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            # Create a unique matric_id
            name = form.cleaned_data['name']
            matric_id = f"A24DW{str(Resident.objects.count() + 1).zfill(4)}"

            # Ensure matric_id is unique (Check if it already exists in User)
            while User.objects.filter(matric_id=matric_id).exists():
                matric_id = f"A24DW{str(Resident.objects.count() + 1).zfill(4)}"

            # Generate a random password for the new user
            password = generate_random_password()

            # Create the user with the given matric_id and password
            user = User.objects.create_user(username=matric_id, password=password)
            user.first_name = name.split()[0]  # Assign first name from 'name'
            user.last_name = name.split()[-1]  # Assign last name from 'name'
            user.save()

            # Assign a role to the user (Resident)
            resident = form.save(commit=False)
            resident.user = user
            resident.save()

            # Redirect to the home page after successful creation
            return redirect('home')
    else:
        form = ResidentForm()

    return render(request, 'create_resident.html', {'form': form})

def matric_login(request):
    if request.method == 'POST':
        matric_id = request.POST['matric_id']
        password = request.POST['password']
        user = authenticate(request, matric_id=matric_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid Matric ID or Password'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')

# New view to handle AJAX request for fetching rooms based on block and level
def get_rooms(request):
    block_id = request.GET.get('block')
    level_id = request.GET.get('level')

    # Ensure block and level IDs are valid
    if not block_id or not level_id:
        return JsonResponse({'error': 'Invalid block or level parameters'}, status=400)

    # Get rooms that match the selected block and level
    rooms = Room.objects.filter(block_id=block_id, level_id=level_id)

    # Prepare room data in a format that can be returned as JSON
    room_data = [{'id': room.id, 'room_number': room.number} for room in rooms]

    return JsonResponse({'rooms': room_data})
