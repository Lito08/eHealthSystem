from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.appointment_list, name='appointment_list'),
    path('edit/<str:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('cancel/<str:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('confirm/<str:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('report-health/', views.report_health, name='report_health'),
    path('manage/', views.manage_appointments, name='manage_appointments'),
]
