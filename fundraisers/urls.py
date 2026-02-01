from django.urls import path
from . import views

app_name = "fundraisers"

urlpatterns = [
    path("announcement/<int:announcement_id>/", views.fundraising_announcement, name="fundraising_announcement"),
    path("create", views.CreateAnnouncementView.as_view(), name="create_announcement"),
    path("announcements", views.AnnouncementsView.as_view(), name="announcements"),
]
