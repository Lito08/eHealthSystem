from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('view_infected_students/', views.view_infected_students, name='view_infected_students'),
    path('view_infected_lecturers/', views.view_infected_lecturers, name='view_infected_lecturers'),
    path('view_hotplaces/', views.view_hotplaces, name='view_hotplaces'),
    path('add_infected_student/', views.add_infected_student, name='add_infected_student'),
    path('add_infected_lecturer/', views.add_infected_lecturer, name='add_infected_lecturer'),
    path('add_hotplace/', views.add_hotplace, name='add_hotplace'),
    # Edit views
    path('edit_infected_person/<int:person_id>/', views.edit_infected_person, name='edit_infected_person'),
    path('edit_hotplace/<int:hotplace_id>/', views.edit_hotplace, name='edit_hotplace'),
    # Delete views
    path('delete_infected_person/<int:person_id>/', views.delete_infected_person, name='delete_infected_person'),
    path('delete_hotplace/<int:hotplace_id>/', views.delete_hotplace, name='delete_hotplace'),
]
