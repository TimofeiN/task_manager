from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    role = models.CharField(
        max_length=50, default=Roles.DEVELOPER, choices=Roles.choices
    )
