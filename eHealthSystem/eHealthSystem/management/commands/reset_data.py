from django.core.management.base import BaseCommand
from eHealthSystem.models import Block, Level, Room

class Command(BaseCommand):
    help = 'Resets the blocks, levels, and rooms data'

    def handle(self, *args, **kwargs):
        # Step 1: Delete all existing blocks, levels, and rooms
        Block.objects.all().delete()
        Level.objects.all().delete()
        Room.objects.all().delete()

        # Step 2: Create new blocks
        block1 = Block.objects.create(name="HB1")
        block2 = Block.objects.create(name="HB2")

        # Step 3: Create new levels (1st to 5th floor)
        levels = [Level.objects.create(name=str(i)) for i in range(1, 6)]

        # Step 4: Create rooms (10 rooms per floor for each block)
        for block in [block1, block2]:
            for level in levels:
                for i in range(1, 11):  # 10 rooms per floor
                    Room.objects.create(block=block, level=level, number=f"{level.name}{i:02d}")

        self.stdout.write(self.style.SUCCESS('Successfully reset data and added new blocks, levels, and rooms'))
