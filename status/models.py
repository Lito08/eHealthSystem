from django.db import models

class InfectedPerson(models.Model):
    name = models.CharField(max_length=255)
    student_or_lecturer = models.CharField(max_length=10, choices=[('student', 'Student'), ('lecturer', 'Lecturer')])
    infected = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Hotplace(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


# Create your models here.
