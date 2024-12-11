from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from eHealthSystem.models import Block, Level, Room, Resident  # Import models
import random
import string

class Command(BaseCommand):
    help = 'Create a superuser automatically if not exists, or delete and recreate if it does.'

    def add_arguments(self, parser):
        # Add arguments for matric_id and password
        parser.add_argument(
            '--matric_id',
            type=str,
            default='A24DW0001',  # Default matric_id
            help='The matric_id for the superuser (default is "A24DW0001")',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='adminpassword',  # Default password
            help='Password for the superuser (default is "adminpassword")',
        )

    def generate_random_matric_id(self):
        """Generate a random matric ID if 'random' is chosen."""
        return f"A24DW{str(random.randint(1, 9999)).zfill(4)}"  # Random matric ID format A24DW####

    def handle(self, *args, **options):
        User = get_user_model()
        matric_id = options['matric_id']
        password = options['password']

        # Generate random matric_id if needed
        if matric_id == 'random':
            matric_id = self.generate_random_matric_id()

        # Define superuser credentials
        superuser_credentials = {
            'matric_id': matric_id,
            'username': matric_id,  # Ensure the username is the same as matric_id
            'password': password,
            'first_name': 'Admin',
            'last_name': 'Superuser',
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True,
            'account_type': 'STA',  # Staff/Admin type
        }

        # Check if superuser already exists
        existing_superuser = User.objects.filter(matric_id=superuser_credentials['matric_id']).first()

        if existing_superuser:
            # Delete the existing superuser
            existing_superuser.delete()
            self.stdout.write(self.style.SUCCESS(f"Existing superuser {superuser_credentials['matric_id']} deleted."))

        # Provide default block, level, and room if Resident is required for superuser
        default_block = Block.objects.first()  # Use the first block available in the database
        default_level = Level.objects.first()  # Use the first level available in the database
        default_room = Room.objects.filter(block=default_block, level=default_level).first()  # Get first room in that block and level

        # Create superuser using the corrected create_superuser method
        try:
            # Create the user (superuser)
            user = User.objects.create_superuser(**superuser_credentials)
            self.stdout.write(self.style.SUCCESS(f"Superuser {superuser_credentials['matric_id']} created successfully."))

            # If Resident is required, create the Resident with default values for block, level, and room
            if default_block and default_level and default_room:
                # Create Resident associated with the superuser
                resident_credentials = {
                    'user': user,
                    'block': default_block,
                    'level': default_level,
                    'room_number': default_room,
                    'account_type': 'STA',  # Staff/Admin type
                }
                Resident.objects.create(**resident_credentials)
                self.stdout.write(self.style.SUCCESS(f"Resident created for superuser {superuser_credentials['matric_id']}."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating superuser: {str(e)}"))
