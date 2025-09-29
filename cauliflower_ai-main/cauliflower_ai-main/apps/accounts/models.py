from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    plain_password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class FarmerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='farmer_profile')
    farm_size = models.FloatField()
    years_farming = models.IntegerField()
    main_crops = models.CharField(max_length=255)
    irrigation_method = models.CharField(max_length=255)

    def __str__(self):
        return f"Farmer: {self.user.username}"


class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False, help_text="Admin approval status")

    def __str__(self):
        return f"Doctor: {self.user.username}"
