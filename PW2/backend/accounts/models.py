from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("STUDENT", "Student"),
        ("TUTOR", "Tutor"),
        ("PC", "Program Coordinator"),
        ("HOD", "Head of Department"),
        ("DEAN", "Academic Dean"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    roll_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
