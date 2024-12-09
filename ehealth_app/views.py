from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UploadedFile
from .forms import FileUploadForm

# Custom login view
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home after login
            else:
                # Invalid credentials
                return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid credentials'})
        else:
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Helper functions for role-based access
def is_resident(user):
    return user.user_type == 'Resident'

def is_admin(user):
    return user.user_type == 'Admin'

def is_clinic(user):
    return user.user_type == 'Clinic'

# Home view
def home(request):
    return render(request, 'home.html')  # Render a home page template

# Resident dashboard
@login_required
@user_passes_test(is_resident, login_url='/login/')
def resident_dashboard(request):
    return render(request, 'resident_dashboard.html')  # Render resident dashboard

# Admin dashboard
@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')  # Render admin dashboard

# Clinic dashboard
@login_required
@user_passes_test(is_clinic, login_url='/login/')
def clinic_dashboard(request):
    return render(request, 'clinic_dashboard.html')  # Render clinic dashboard

# File upload view
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the uploaded file to the database
            return redirect('home')  # Redirect to home page after successful upload
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

# File download view
def download_file(request, file_id):
    file = get_object_or_404(UploadedFile, pk=file_id)
    response = HttpResponse(file.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={file.file.name}'
    return response

# Define a simple algorithm function for eligibility check
def check_eligibility(age):
    """
    Simple algorithm to check eligibility based on age.
    If age is 18 or more, return 'Eligible'.
    If age is less than 18, return 'Not Eligible'.
    """
    if age >= 18:
        return "Eligible"
    else:
        return "Not Eligible"

# View for eligibility check
def eligibility_check(request):
    eligibility = None

    if request.method == 'POST':
        try:
            age = int(request.POST.get('age'))
        except ValueError:
            eligibility = "Invalid age input"
        else:
            eligibility = check_eligibility(age)

    return render(request, 'ehealth_app/eligibility_check.html', {'eligibility': eligibility})
