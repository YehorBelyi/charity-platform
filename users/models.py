from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from verifications.models import VerificationRequest

# Create your models here.
class CustomUser(AbstractUser):
    date_of_birth = models.DateTimeField(default=timezone.now, blank=True, null=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def is_verified(self):
        return self.verification_requests.filter(
            status=VerificationRequest.Status.APPROVED
        ).exists()

    def __str__(self):
        return self.username