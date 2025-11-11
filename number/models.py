from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add any additional fields here if necessary
    # For example: phone_number = models.CharField(max_length=15, blank=True, null=True)
    pass