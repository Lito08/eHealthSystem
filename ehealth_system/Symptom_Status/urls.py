from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.symptom_reporting, name='symptom_reporting'),
    path('status/', views.health_status, name='health_status'),
    path('quarantine/', views.quarantine_management, name='quarantine_management'),
    path('edit/<int:resident_id>/', views.edit_resident, name='edit_resident'),
    path('delete/<int:resident_id>/', views.delete_resident, name='delete_resident'),
]