from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from .models import FundraisingAnnouncement
from .forms import AddFundraisingAnnouncementForm

def fundraising_announcement(request, announcement_id):
    announcement = get_object_or_404(FundraisingAnnouncement, pk=announcement_id)

    context = {
        "announcement": announcement
    }
    return render(request, "fundraisers/announcement.html", context)


class CreateAnnouncementView(CreateView):
    template_name = "fundraisers/create_announcement.html"
    model = FundraisingAnnouncement
    form_class = AddFundraisingAnnouncementForm
    success_url = "/"
