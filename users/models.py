from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

from django import forms


# Create your models here.
class CustomUser(AbstractUser):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    date_of_birth = models.DateTimeField(default=timezone.now, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number']