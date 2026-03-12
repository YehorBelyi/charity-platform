from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from verifications.models import VerificationRequest

STATUS_CHOICES = (
    ('civilian', 'Civilian'),
    ('volunteer', 'Volunteer'),
    ('soldier', 'Soldier'),
)


RANK_CHOICES = (
    ('none', 'None'),
    ('private', 'Private'),
    ('officer', 'Officer'),
)


class CustomUser(AbstractUser):

    date_of_birth = models.DateTimeField(default=timezone.now, blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=False, default='none')
    rank = models.CharField(max_length=30, choices=RANK_CHOICES, null=True, blank=False, default='none')

    def is_verified(self):
        return self.verification_requests.filter(
            status=VerificationRequest.Status.APPROVED
        ).exists()

    def __str__(self):
        return self.username

