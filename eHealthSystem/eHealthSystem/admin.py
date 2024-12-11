from django.contrib import admin
from .models import User, Resident

class ResidentInline(admin.StackedInline):
    model = Resident
    extra = 1
    can_delete = False  # Disable delete option for Resident records in the User admin view

class UserAdmin(admin.ModelAdmin):
    inlines = [ResidentInline]
    list_display = ['matric_id', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'get_account_type']
    search_fields = ['matric_id', 'first_name', 'last_name']

    def get_account_type(self, obj):
        # Access the account_type of the related Resident object
        return obj.resident.account_type if hasattr(obj, 'resident') else None
    get_account_type.short_description = 'Account Type'  # Display name for the column

admin.site.register(User, UserAdmin)
admin.site.register(Resident)
