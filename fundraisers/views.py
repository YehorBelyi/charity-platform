"""Django views for fundraisers app"""
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, ListView
from reports.models import Report
from .forms import AddUpdateFundraisingAnnouncementForm, SearchForm
from .models import FundraisingAnnouncement


def fundraising_announcement(request, announcement_id):
    """Get requested announcement and render corresponding template."""
    announcement = get_object_or_404(FundraisingAnnouncement, pk=announcement_id)
    payment_status = request.GET.get("payment_status")
    payment_amount = request.GET.get("payment_amount")
    report = Report.objects.filter(fundraising_announcement=announcement).first()

    context = {
        "announcement": announcement,
        "payment_status": payment_status,
        "payment_amount": payment_amount,
        "report": report,
    }
    return render(request, "fundraisers/announcement.html", context)


class CreateAnnouncementView(LoginRequiredMixin, CreateView):
    """Handle form for creating a new fundraising announcement."""
    template_name = "fundraisers/create_update_announcement.html"
    model = FundraisingAnnouncement
    form_class = AddUpdateFundraisingAnnouncementForm
    success_url = "/"
    login_url = "/users/login/"

    def dispatch(self, request, *args, **kwargs):
        """Allow only verified users to create fundraisers."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_verified():
            messages.warning(
                request,
                "Щоб створити власний збір, спершу пройдіть верифікацію."
            )
            return redirect("verification_create")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Set current user as the author of the form."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnnouncementsView(ListView):
    """Display list of announcements."""
    template_name = "fundraisers/announcements.html"
    queryset = FundraisingAnnouncement.objects.filter(is_closed=False)
    paginate_by = 15
    ordering = "-date"

    def get_context_data(self, **kwargs):
        """Add SearchForm and query_params to the context."""
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm(self.request.GET)

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = query_params.urlencode()

        return context

    def get_queryset(self):
        """Filter and sort queryset by user search request."""

        search = self.request.GET.get("search") or ""
        queryset = super().get_queryset().filter(title__icontains=search)
        ordering = self.request.GET.get("ordering")

        if ordering == "newest":
            queryset = queryset.order_by("-date")
        elif ordering == "biggest":
            queryset = queryset.order_by("-target_sum")
        else:
            # Calculate the total amount of donations for each announcement over the last few days
            queryset = queryset.annotate(
                recent_payments_sum=Sum(
                    "payments__amount",
                    filter=Q(payments__date__gt=timezone.now().date() - datetime.timedelta(days=2))
                )
            )

            queryset = queryset.order_by("-recent_payments_sum")

        return queryset


class UserAnnouncementsPartialView(LoginRequiredMixin, ListView):
    """Display current users list of announcements."""
    model = FundraisingAnnouncement
    template_name = "components/user_announcements.html"
    context_object_name = "announcements"

    def get_queryset(self):
        return (
            FundraisingAnnouncement.objects.filter(author=self.request.user)
            .prefetch_related("report_set")
            .order_by("-date")
        )


@login_required
def update_announcement(request, announcement_id):
    """Update selected announcement."""
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


@login_required
def delete_announcement(request, announcement_id):
    """Delete selected announcement owned by the current user."""
    if request.method != "POST":
        return HttpResponse(status=405)

    announcement = get_object_or_404(FundraisingAnnouncement, pk=announcement_id)

    if announcement.author != request.user:
        return HttpResponse(status=403)

    announcement.delete()
    return redirect("profile")


@login_required
def close_announcement(request, announcement_id):
    """Close an announcement after the fundraising goal has been reached."""
    if request.method != "POST":
        return HttpResponse(status=405)

    announcement = get_object_or_404(FundraisingAnnouncement, pk=announcement_id)

    if announcement.author != request.user:
        return HttpResponse(status=403)

    if announcement.is_closed:
        messages.info(request, "Цей збір уже закрито.")
        return redirect("fundraisers:fundraising_announcement", announcement_id=announcement.id)

    if not announcement.is_target_reached:
        messages.warning(request, "Закрити збір можна лише після досягнення цільової суми.")
        return redirect("fundraisers:fundraising_announcement", announcement_id=announcement.id)

    announcement.is_closed = True
    announcement.save(update_fields=["is_closed"])
    messages.success(request, "Збір закрито. Тепер ви можете створити звіт за бажанням.")
    return redirect("fundraisers:fundraising_announcement", announcement_id=announcement.id)
