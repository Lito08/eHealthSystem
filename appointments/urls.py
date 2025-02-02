from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('get-available-slots/', views.get_available_slots, name='get_available_slots'),
    path('my-appointments/', views.appointment_list, name='appointment_list'),
    path('edit/<str:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('cancel/<str:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('update-result/<str:appointment_id>/', views.update_appointment_result, name='update_appointment_result'),
    path('report-health/', views.report_health, name='report_health'),
    path('manage/', views.manage_appointments, name='manage_appointments'),
]
