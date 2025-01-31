from django.urls import path
from . import views

urlpatterns = [
    path('', views.hostel_list, name='hostel_list'),
    path('add/', views.add_hostel, name='add_hostel'),
    path('<int:hostel_id>/edit/', views.edit_hostel, name='edit_hostel'),
    path('<int:hostel_id>/delete/', views.delete_hostel, name='delete_hostel'),
    path('<int:hostel_id>/rooms/', views.room_list, name='room_list'),
    path('room/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('room/<int:room_id>/delete/', views.delete_room, name='delete_room'),
]
