import random
import string
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(DefaultUserManager):
    def generate_random_password(self, length=8):
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def create_user(self, matric_id, password=None, account_type='STU', block='HB1', level='1', room_number='101', **extra_fields):
        """
        Create and return a regular user with an associated Resident.
        """
        if not matric_id:
            raise ValueError(_('The Matric ID must be set'))

        if not password:
            password = self.generate_random_password()  # Generate random password if not provided

        # Create the user with matric_id and extra fields
        user = self.model(matric_id=matric_id, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)

        # Import Resident models here to avoid circular import
        from .models import Resident  # Import here to avoid circular import
        resident = Resident.objects.create(
            user=user,
            account_type=account_type,
            block=block,  # Ensure a value for block is passed
            level=level,  # Ensure a value for level is passed
            room_number=room_number  # Ensure a value for room_number is passed
        )

        return user

    def create_superuser(self, matric_id, password=None, **extra_fields):
        """
        Create and return a superuser (admin), without any associated Resident attributes.
        """
        if not matric_id:
            raise ValueError(_('Superuser must have a matric ID'))

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('account_type', 'STA')  # Set the account type to STAFF for superuser
        extra_fields.setdefault('block', None)  # No block for superuser
        extra_fields.setdefault('level', None)  # No level for superuser
        extra_fields.setdefault('room_number', None)  # No room number for superuser

        # Only pass matric_id, password, and extra_fields to create_user
        user = self.create_user(matric_id=matric_id, password=password, **extra_fields)

        # Return the created superuser
        return user
