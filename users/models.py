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
    """
    Custom user model for the application.

    Extends the standard Django AbstractUser to include profile information
    such as avatar, status (civilian/volunteer/soldier), and verification status.
    """

    #: Profile picture of the user.
    avatar = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    #: User's date of birth.
    date_of_birth = models.DateField(default=timezone.now, blank=True, null=True)

    #: Contact phone number.
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    #: Social status of the user (e.g., Civilian, Volunteer).
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=False, default='none')

    #: Military or organizational rank.
    rank = models.CharField(max_length=30, choices=RANK_CHOICES, null=True, blank=False, default='none')

    #: Short information about user.
    short_bio = models.CharField(max_length=200, null=True)

    def is_verified(self):
        """
        Check if the user has an approved verification request.

        Returns:
            bool: True if at least one approved request exists, False otherwise.
        """
        return self.verification_requests.filter(
            status=VerificationRequest.Status.APPROVED
        ).exists()

    def __str__(self):
        return self.username

