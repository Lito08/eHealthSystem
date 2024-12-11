from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager  # Import the custom manager at the top

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
    number = models.CharField(max_length=5)

    def save(self, *args, **kwargs):
        # Automatically generate room number based on block and level
        if not self.number:
            floor_number = str(self.level.name).zfill(3)  # Ensure the level is always 3 digits
            room_number = str(self.block.name) + floor_number + str(self.pk).zfill(2)  # Room number format
            self.number = room_number
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.block.name} {self.level.name} {self.number}"

class User(AbstractUser):
    matric_id = models.CharField(max_length=10, unique=True)

    # Assign the custom manager directly to the User model
    objects = UserManager()  # Directly assign the custom manager

    def __str__(self):
        return self.matric_id

class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Reference as a string
    account_type = models.CharField(
        max_length=3, choices=AccountType.choices, default=AccountType.STUDENT
    )
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.block.name} {self.level.name} {self.room_number.number}"
