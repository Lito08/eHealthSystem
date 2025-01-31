import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """Redirects admins to the dashboard while allowing residents to view the homepage."""
    if request.user.role in ['superadmin', 'admin']:
        return redirect('dashboard')  # Redirect admins to dashboard
    return render(request, 'home.html')  # Residents see home page

@login_required
def dashboard(request):
    template_dirs = settings.TEMPLATES[0]['DIRS']
    print(f"Looking for templates in: {template_dirs}")
    return render(request, 'dashboard.html')
