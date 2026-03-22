"""
Django admin configuration for the fundraisers application.

Registers models in the admin interface to allow staff users
to view and manage fundraisers records.
"""

from django.contrib import admin
from .models import FundraisingAnnouncement

#: Register the FundraisingAnnouncement model in the Django Admin site.
admin.site.register(FundraisingAnnouncement)
