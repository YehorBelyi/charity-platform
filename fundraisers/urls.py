from django.urls import path
from . import views

urlpatterns = [
    path("announcement/<int:announcement_id>/", views.fundraising_announcement, name="fundraising_announcement"),
    path("create", views.CreateAnnouncementView.as_view(), name="create_announcement"),
]
