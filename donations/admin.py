"""
Django admin configuration for the donations application.

Registers models in the admin interface to allow staff users
to view and manage payment records.
"""

from django.contrib import admin

from donations.models import Payment

# Register your models here.

#: Register the Payment model in the Django Admin site.
admin.site.register(Payment)
