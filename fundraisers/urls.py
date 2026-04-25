"""
URL configuration for the fundraisers application.

This module defines view routes for:
- Announcement page.
- Page for creating announcements.
- Page with all announcements.
"""

from django.urls import path
from . import views

app_name = "fundraisers"

urlpatterns = [
    path(
        "announcement/<int:announcement_id>/",
        views.fundraising_announcement,
        name="fundraising_announcement"
    ),
    path("create", views.CreateAnnouncementView.as_view(), name="create_announcement"),
    path("announcements", views.AnnouncementsView.as_view(), name="announcements"),
    path("list", views.UserAnnouncementsPartialView.as_view(), name="user_announcements"),
    path("update/<int:announcement_id>", views.update_announcement, name="update_announcement"),
    path("delete/<int:announcement_id>", views.delete_announcement, name="delete_announcement"),
]
