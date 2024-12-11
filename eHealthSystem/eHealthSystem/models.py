from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Define the possible account types for clarity and easy use in the system
class AccountType(models.TextChoices):
    STUDENT = 'STU', 'Student'
    LECTURER = 'LEC', 'Lecturer'
    STAFF = 'STA', 'Staff'

class Block(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class Room(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    number = models.CharField(max_length=5, blank=True)

    class Meta:
        unique_together = ('block', 'level', 'number')  # Ensure unique room number within a block and level

    def save(self, *args, **kwargs):
        """
        Automatically generate room number based on block and level if not explicitly set.
        """
        if not self.number:
            floor_number = self.level.name.zfill(2)  # Ensure the level is 2 digits
            # Generate room index based on existing rooms in the same block and level
            room_index = Room.objects.filter(block=self.block, level=self.level).count() + 1
            self.number = f"{self.block.name}{floor_number}{str(room_index).zfill(2)}"  # Room format: BlockLevelXX

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.block.name} {self.level.name} {self.number}"

class User(AbstractUser):
    matric_id = models.CharField(max_length=10, unique=True)

    objects = UserManager()  # Assign custom user manager

    def __str__(self):
        return f"{self.matric_id} - {self.first_name} {self.last_name}"

class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resident')
    account_type = models.CharField(
        max_length=3, choices=AccountType.choices, default=AccountType.STUDENT
    )
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.account_type} - Room {self.room_number.number}"
