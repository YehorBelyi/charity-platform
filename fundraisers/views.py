"""Django views for fundraisers app"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView
from .models import FundraisingAnnouncement
from .forms import AddUpdateFundraisingAnnouncementForm, SearchForm


def fundraising_announcement(request, announcement_id):
    """Get requested announcement and render corresponding template."""
    announcement = get_object_or_404(FundraisingAnnouncement, pk=announcement_id)

    context = {
        "announcement": announcement
    }
    return render(request, "fundraisers/announcement.html", context)


class CreateAnnouncementView(LoginRequiredMixin, CreateView):
    """Handle form for creating a new fundraising announcement."""
    template_name = "fundraisers/create_update_announcement.html"
    model = FundraisingAnnouncement
    form_class = AddUpdateFundraisingAnnouncementForm
    success_url = "/"
    login_url = "/users/login/"

    def form_valid(self, form):
        """Set current user as the author of the form."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnnouncementsView(ListView):
    """Display list of announcements."""
    template_name = "fundraisers/announcements.html"
    queryset = FundraisingAnnouncement.objects.all()
    paginate_by = 15
    ordering = "-date"

    def get_context_data(self, **kwargs):
        """Add SearchForm to the context."""
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm(self.request.GET)
        return context

    def get_queryset(self):
        """Filter queryset by user search request."""
        queryset = super().get_queryset()
        return queryset.filter(title__icontains=self.request.GET.get("search") or "")

class UserAnnouncementsPartialView(LoginRequiredMixin, ListView):
    """Display current users list of announcements."""
    model = FundraisingAnnouncement
    template_name = 'components/user_announcements.html'
    context_object_name = "announcements"

    def get_queryset(self):
        return FundraisingAnnouncement.objects.filter(author=self.request.user).order_by("-date")


@login_required
def update_announcement(request, announcement_id):
    """Update selected announcement"""
    announcement = get_object_or_404(FundraisingAnnouncement, pk=announcement_id)

    if announcement.author != request.user:
        return HttpResponse(status=403)

    if request.method == "GET":
        form = AddUpdateFundraisingAnnouncementForm(instance=announcement)
        return render(request, "fundraisers/create_update_announcement.html", {"form": form})

    if request.method == "POST":
        form = AddUpdateFundraisingAnnouncementForm(
            request.POST, request.FILES, instance=announcement
        )

        if form.is_valid():
            form.save()
            return render(request, "pages/success_alert.html", {"text": "Збір оновлено успішно"})

        return render(request, "fundraisers/create_update_announcement.html", {"form": form})
    return HttpResponse(status=400)
