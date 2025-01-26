from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('matric_id', 'email', 'role', 'is_active', 'is_staff')
    search_fields = ('matric_id', 'email', 'role')
    list_filter = ('role', 'is_active', 'is_staff')
    ordering = ('matric_id',)
    fieldsets = (
        (None, {'fields': ('matric_id', 'password')}),
        ('Personal info', {'fields': ('email', 'phone_number', 'hostel_block')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matric_id', 'email', 'role', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
