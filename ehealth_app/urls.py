from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload'),
    path('download/<int:file_id>/', views.download_file, name='download'),
    path('eligibility-check/', views.eligibility_check, name='eligibility_check'),
    path('resident-dashboard/', views.resident_dashboard, name='resident_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('clinic-dashboard/', views.clinic_dashboard, name='clinic_dashboard'),
]
