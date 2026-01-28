from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    date_of_birth = models.DateTimeField()
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=30)

    def __str__(self):
        return self.username