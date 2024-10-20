

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("landlord", "Landlord"),
    ]

    # Ensuring that role is mandatory and can't be null
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, null=False, default="student"
    )

    # UUIDField ensures unique verification token
    verification_token = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
