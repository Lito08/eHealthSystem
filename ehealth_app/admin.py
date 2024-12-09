from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UploadedFile, CustomUser

# Register the UploadedFile model
@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')  # Display these fields in the admin list view
    search_fields = ('file',)  # Enable search by file name

# Customizing the CustomUser admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the list view
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')

    # Add filters for easy navigation
    list_filter = ('user_type', 'is_staff', 'is_active', 'is_superuser')

    # Define search fields for the admin search bar
    search_fields = ('username', 'email')

    # Customize the user add/edit forms
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('User Type', {'fields': ('user_type',)}),  # Add the custom user_type field
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Customize the fields for the "add user" form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'is_staff', 'is_active'),
        }),
    )
