"""
Admin interface registration for the units app.
"""

from django.contrib import admin
from .models import Unit

#: Registers the Unit model to allow management of the organizational tree.
admin.site.register(Unit)
