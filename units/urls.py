from django.urls import path
from . import views

app_name = "units"

urlpatterns = [
    path("unit/<int:unit_id>/", views.unit, name = "unit"),
]