"""
URL configuration for the units application.

Defines routes for viewing individual unit details and their organizational data.
"""

from django.urls import path
from . import views

app_name = "units"

urlpatterns = [
    #: Route for the unit detail page, identified by its numeric ID.
    path("unit/<int:unit_id>/", views.unit, name = "unit"),
]