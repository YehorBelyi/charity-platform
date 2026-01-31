from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView
from .models import FundraisingAnnouncement
from .forms import AddFundraisingAnnouncementForm

def fundraising_announcement(request, announcement_id):
    announcement = get_object_or_404(FundraisingAnnouncement, pk=announcement_id)

    context = {
        "announcement": announcement
    }
    return render(request, "fundraisers/announcement.html", context)


class CreateAnnouncementView(LoginRequiredMixin, CreateView):
    template_name = "fundraisers/create_announcement.html"
    model = FundraisingAnnouncement
    form_class = AddFundraisingAnnouncementForm
    success_url = "/"
    login_url = "/users/login/"

    # add user to the form
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnnouncementsView(ListView):
    template_name = "fundraisers/announcements.html"
    queryset = FundraisingAnnouncement.objects.all()
    paginate_by = 15