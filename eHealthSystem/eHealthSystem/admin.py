from django.contrib import admin
from .models import User, Resident

# Inline for linking Resident to User
class ResidentInline(admin.StackedInline):
    model = Resident
    extra = 0  # Do not show extra blank forms by default
    can_delete = False  # Disable deletion of Resident records through User admin
    readonly_fields = ['account_type', 'block', 'level', 'room_number']  # Make fields read-only for consistency

# Custom admin for User model
class UserAdmin(admin.ModelAdmin):
    inlines = [ResidentInline]  # Add Resident details inline
    list_display = ['matric_id', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'get_account_type']
    search_fields = ['matric_id', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_superuser']  # Add filters for user roles

    def get_account_type(self, obj):
        """
        Display the account type of the related Resident object.
        """
        return getattr(obj.resident, 'account_type', 'N/A')  # Use getattr to avoid AttributeError
    get_account_type.short_description = 'Account Type'  # Set a user-friendly name for the column

# Register the admin views
admin.site.register(User, UserAdmin)
admin.site.register(Resident)
