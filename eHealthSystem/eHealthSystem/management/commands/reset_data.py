from django.core.management.base import BaseCommand
from eHealthSystem.models import Block, Level, Room
from django.db import connection

class Command(BaseCommand):
    help = 'Resets the blocks, levels, and rooms data'

    def handle(self, *args, **kwargs):
        # Step 1: Delete all existing blocks, levels, and rooms (with confirmation)
        self.stdout.write(self.style.WARNING('Deleting all existing blocks, levels, and rooms...'))
        Room.objects.all().delete()  # Ensure rooms are deleted first
        Level.objects.all().delete()  # Delete levels
        Block.objects.all().delete()  # Delete blocks

        # Reset the auto-increment ID counters for each table (use this for SQLite)
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='eHealthSystem_block';")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='eHealthSystem_level';")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='eHealthSystem_room';")

        self.stdout.write(self.style.SUCCESS('Auto-increment counters reset successfully.'))

        # Step 2: Create new blocks
        block1 = Block.objects.create(name="HB1")
        block2 = Block.objects.create(name="HB2")
        self.stdout.write(self.style.SUCCESS(f'Successfully created blocks: {block1.name} and {block2.name}.'))

        # Step 3: Create new levels (1st to 5th floor)
        levels = [Level.objects.create(name=str(i)) for i in range(1, 6)]
        self.stdout.write(self.style.SUCCESS('Successfully created levels 1 to 5.'))

        # Step 4: Create rooms (10 rooms per floor for each block)
        for block in [block1, block2]:
            self.stdout.write(self.style.SUCCESS(f"Creating rooms for block {block.name}..."))
            for level in levels:
                for i in range(1, 11):  # 10 rooms per floor
                    room_number = f"{level.name}{i:02d}"  # Format room number (e.g., '101', '102', etc.)
                    
                    # Check if the room already exists
                    existing_room = Room.objects.filter(block=block, level=level, number=room_number).first()
                    if not existing_room:
                        Room.objects.create(block=block, level=level, number=room_number)
                        self.stdout.write(self.style.SUCCESS(f"Room {room_number} created in block {block.name}."))
                    else:
                        self.stdout.write(self.style.WARNING(f"Room {room_number} already exists in block {block.name}, skipping..."))

        self.stdout.write(self.style.SUCCESS('Successfully reset data and added new blocks, levels, and rooms.'))
