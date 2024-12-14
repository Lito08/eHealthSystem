from django.shortcuts import render, redirect, get_object_or_404
from .models import InfectedPerson, Hotplace, InfectedPerson
from django.http import HttpResponse
from .forms import InfectedPersonForm

# Main page
def main_page(request):
    infected_students = InfectedPerson.objects.filter(student_or_lecturer='student', infected=True).count()
    infected_lecturers = InfectedPerson.objects.filter(student_or_lecturer='lecturer', infected=True).count()
    hotplaces = Hotplace.objects.all()

    return render(request, 'status/main_page.html', {
        'infected_students': infected_students,
        'infected_lecturers': infected_lecturers,
        'hotplaces': hotplaces,
        
    })

# View infected students
def view_infected_students(request):
    infected_students = InfectedPerson.objects.filter(student_or_lecturer='student')
    return render(request, 'status/view_infected_students.html', {'infected_students': infected_students})

# View infected lecturers
def view_infected_lecturers(request):
    infected_lecturers = InfectedPerson.objects.filter(student_or_lecturer='lecturer')
    return render(request, 'status/view_infected_lecturers.html', {'infected_lecturers': infected_lecturers})

# View and manage hotplaces
def view_hotplaces(request):
    hotplaces = Hotplace.objects.all()
    return render(request, 'status/view_hotplaces.html', {'hotplaces': hotplaces})

from django.shortcuts import render, redirect
from .models import InfectedPerson, Hotplace
from .forms import InfectedPersonForm, HotplaceForm

# View to add a new infected student
def add_infected_student(request):
    if request.method == 'POST':
        form = InfectedPersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_infected_students')
    else:
        form = InfectedPersonForm()
    return render(request, 'status/add_infected_student.html', {'form': form})

# View to add a new infected lecturer
def add_infected_lecturer(request):
    if request.method == 'POST':
        form = InfectedPersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_infected_lecturers')
    else:
        form = InfectedPersonForm()
    return render(request, 'status/add_infected_lecturer.html', {'form': form})

# View to add a new hotplace
def add_hotplace(request):
    if request.method == 'POST':
        form = HotplaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_page')
    else:
        form = HotplaceForm()
    return render(request, 'status/add_hotplace.html', {'form': form})

def edit_infected_person(request, person_id):
    infected_person = get_object_or_404(InfectedPerson, pk=person_id)
    if request.method == 'POST':
        form = InfectedPersonForm(request.POST, instance=infected_person)
        if form.is_valid():
            form.save()
            return redirect('view_infected_students')  # Redirect to the infected students list page
    else:
        form = InfectedPersonForm(instance=infected_person)
    return render(request, 'status/edit_infected_person.html', {'form': form, 'person': infected_person})

def edit_hotplace(request, hotplace_id):
    hotplace = get_object_or_404(Hotplace, pk=hotplace_id)
    if request.method == 'POST':
        form = HotplaceForm(request.POST, instance=hotplace)
        if form.is_valid():
            form.save()
            return redirect('view_hotplaces')  # Redirect to the hotplaces list page
    else:
        form = HotplaceForm(instance=hotplace)
    return render(request, 'status/edit_hotplace.html', {'form': form, 'hotplace': hotplace})

def delete_infected_person(request, person_id):
    infected_person = get_object_or_404(InfectedPerson, pk=person_id)
    infected_person.delete()
    return redirect('view_infected_students')  # Redirect to the infected students list page

# View to delete a hotplace
def delete_hotplace(request, hotplace_id):
    hotplace = get_object_or_404(Hotplace, pk=hotplace_id)
    hotplace.delete()
    return redirect('main_page')  # Redirect to the hotplaces list page



# Create your views here.
