from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import ResidentForm
from .models import Resident, User, Room, Block, Level  # Import Block and Level here
from .utils import generate_matric_id
import random
import string

# Utility function to generate random passwords
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

@login_required
def create_resident(request):
    # Only superusers (admins) can create residents
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        form = ResidentForm(request.POST, user=request.user)  # Pass the current user to the form
        if form.is_valid():
            try:
                # Get the block and level selections
                block_id = form.cleaned_data['block']
                level_id = form.cleaned_data['level']

                # Ensure that the selected block and level exist in the database
                block = Block.objects.get(id=block_id)  # Retrieve the actual Block instance
                level = Level.objects.get(id=level_id)  # Retrieve the actual Level instance

                # Get the matric_id from the form (it may be dynamically generated)
                matric_id = form.cleaned_data['matric_id']

                # Ensure matric_id is unique
                while User.objects.filter(matric_id=matric_id).exists():
                    matric_id = f"A24DW{str(int(matric_id[5:]) + 1).zfill(4)}"  # Increment matric_id if it already exists

                # Generate a random password for the new user
                password = generate_random_password()

                # Create the user with the given matric_id and password
                user = User.objects.create_user(
                    username=matric_id,  # Set the matric_id as the username
                    password=password,
                    matric_id=matric_id  # Pass matric_id as a separate field
                )
                user.first_name = form.cleaned_data['first_name']  # Assign first name from form
                user.last_name = form.cleaned_data['last_name']  # Assign last name from form
                user.save()

                # Now create the Resident instance and link it to the user
                resident = form.save(commit=False)
                resident.user = user  # Associate the Resident with the User
                resident.block = block  # Assign the Block instance to the Resident
                resident.level = level  # Assign the Level instance to the Resident
                resident.save()  # Save the Resident object, which contains the account_type

                # Redirect to the home page after successful creation
                return redirect('home')
            except Block.DoesNotExist:
                form.add_error('block', "The selected block does not exist.")
            except Level.DoesNotExist:
                form.add_error('level', "The selected level does not exist.")
            except Exception as e:
                # Log the error and show an error message in case something fails
                print(f"Error: {e}")
                form.add_error(None, "There was an error creating the resident. Please try again.")
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = ResidentForm(user=request.user)  # Pass the current user to the form

    return render(request, 'create_resident.html', {'form': form})

def update_matric_id(request):
    account_type = request.GET.get('account_type')
    if account_type:
        matric_id = generate_matric_id(account_type)
        return JsonResponse({'matric_id': matric_id})
    return JsonResponse({'error': 'Invalid account type'}, status=400)

def matric_login(request):
    if request.method == 'POST':
        matric_id = request.POST.get('matric_id')
        password = request.POST.get('password')
        user = authenticate(request, username=matric_id, password=password)
        if user:
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'error': 'Invalid Matric ID or Password'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'home.html')

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
