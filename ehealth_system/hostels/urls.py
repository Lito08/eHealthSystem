from django.urls import path
from . import views

urlpatterns = [
    path('', views.hostel_list, name='hostel_list'),
    path('add/', views.add_hostel, name='add_hostel'),
    path('<int:hostel_id>/rooms/', views.room_list, name='room_list'),  # Add this line
]
