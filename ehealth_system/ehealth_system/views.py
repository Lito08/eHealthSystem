import os
from django.conf import settings
from django.shortcuts import render  # Import the required render function
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    template_dirs = settings.TEMPLATES[0]['DIRS']
    print(f"Looking for templates in: {template_dirs}")
    return render(request, 'dashboard.html')
