from django.urls import path
from . import views

urlpatterns = [
    path("announcement/<int:announcement_id>/", views.fundraising_announcement, name="fundraising_announcement")
]
