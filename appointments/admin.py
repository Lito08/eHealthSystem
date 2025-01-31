from django.contrib import admin
from .models import Clinic, Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('resident', 'clinic', 'appointment_date', 'status')
    list_filter = ('status', 'clinic')
    search_fields = ('resident__username', 'clinic__name')

admin.site.register(Clinic)
admin.site.register(Appointment, AppointmentAdmin)
