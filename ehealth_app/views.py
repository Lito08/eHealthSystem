from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import UploadedFile
from .forms import FileUploadForm

def home(request):
    return render(request, 'home.html')  # Render a home page template

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

# View to accept input from the user and run the algorithm
def eligibility_check(request):
    eligibility = None

    if request.method == 'POST':
        # Get the age from the submitted form
        age = int(request.POST.get('age'))

        # Call the check_eligibility function
        eligibility = check_eligibility(age)

    # Render the template with the eligibility status
    return render(request, 'ehealth_app/eligibility_check.html', {'eligibility': eligibility})