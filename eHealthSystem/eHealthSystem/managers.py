import random
import string
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(DefaultUserManager):
    def generate_random_password(self, length=8):
        """
        Generate a random password of specified length.
        """
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def create_user(self, matric_id, password=None, account_type='STU', block='HB1', level='1', room_number='101', **extra_fields):
        """
        Create and return a regular user with an associated Resident.
        """
        if not matric_id:
            raise ValueError(_('The Matric ID must be set'))

        # Generate a random password if not provided
        password = password or self.generate_random_password()

        # Create the user
        user = self.model(matric_id=matric_id, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)

        # Create and associate a Resident object
        from .models import Resident  # Import locally to avoid circular dependencies
        Resident.objects.create(
            user=user,
            account_type=account_type,
            block=block,
            level=level,
            room_number=room_number
        )

        return user

    def create_superuser(self, matric_id, password=None, **extra_fields):
        """
        Create and return a superuser (admin) without an associated Resident.
        """
        if not matric_id:
            raise ValueError(_('The Matric ID must be set for a superuser'))

        # Set default values for a superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Create the superuser
        return self.model.objects.create_user(
            matric_id=matric_id,
            password=password or self.generate_random_password(),  # Generate a random password if not provided
            **extra_fields
        )
