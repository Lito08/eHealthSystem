from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_terms, name='view_terms'),  # Resident View
    path('manage/', views.manage_terms, name='manage_terms'),  # Admin Management
]
