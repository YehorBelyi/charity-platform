from django.shortcuts import render, get_object_or_404
from .models import FundraisingAnnouncement

def fundraising_announcement(request, announcement_id):
    announcement = get_object_or_404(FundraisingAnnouncement, pk=announcement_id)

    context = {
        "announcement": announcement
    }
    return render(request, "fundraisers/announcement.html", context)
