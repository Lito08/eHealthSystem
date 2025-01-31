from django.contrib import admin
from .models import Hostel, Room

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'block', 'levels', 'rooms_per_level')
    inlines = [RoomInline]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hostel', 'number')
