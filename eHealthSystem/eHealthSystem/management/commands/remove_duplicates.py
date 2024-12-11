from django.core.management.base import BaseCommand
from django.db import models
from eHealthSystem.models import Block, Level, Room

class Command(BaseCommand):
    help = 'Remove duplicate blocks, levels, and rooms from the database'

    def handle(self, *args, **kwargs):
        # Remove duplicate blocks
        blocks = Block.objects.values('name').annotate(name_count=models.Count('name')).filter(name_count__gt=1)
        for block in blocks:
            duplicates = Block.objects.filter(name=block['name'])
            duplicates_to_delete = duplicates[1:]  # Exclude the first entry
            for duplicate in duplicates_to_delete:
                duplicate.delete()  # Delete each duplicate individually
        
        # Remove duplicate levels
        levels = Level.objects.values('name').annotate(name_count=models.Count('name')).filter(name_count__gt=1)
        for level in levels:
            duplicates = Level.objects.filter(name=level['name'])
            duplicates_to_delete = duplicates[1:]  # Exclude the first entry
            for duplicate in duplicates_to_delete:
                duplicate.delete()  # Delete each duplicate individually
        
        # Remove duplicate rooms
        rooms = Room.objects.values('block', 'level', 'number').annotate(room_count=models.Count('id')).filter(room_count__gt=1)
        for room in rooms:
            duplicates = Room.objects.filter(block=room['block'], level=room['level'], number=room['number'])
            duplicates_to_delete = duplicates[1:]  # Exclude the first entry
            for duplicate in duplicates_to_delete:
                duplicate.delete()  # Delete each duplicate individually
        
        self.stdout.write(self.style.SUCCESS('Successfully removed duplicates'))
