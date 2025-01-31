from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TermsAndConditions
from django.contrib import messages

@login_required
def manage_terms(request):
    if request.user.role not in ['admin', 'superadmin']:
        messages.error(request, "You are not authorized to edit Terms & Conditions.")
        return redirect('home')

    terms = TermsAndConditions.objects.first()  # Get latest terms

    if request.method == 'POST':
        content = request.POST.get('content')
        if not content:
            messages.error(request, "Terms & Conditions cannot be empty.")
            return redirect('manage_terms')

        if terms:
            terms.content = content
            terms.save()
        else:
            TermsAndConditions.objects.create(content=content)

        messages.success(request, "Terms & Conditions updated successfully.")
        return redirect('manage_terms')

    return render(request, 'terms/manage_terms.html', {'terms': terms})

def view_terms(request):
    terms = TermsAndConditions.objects.first()
    return render(request, 'terms/view_terms.html', {'terms': terms})
