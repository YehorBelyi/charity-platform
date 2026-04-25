from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from fundraisers.models import FundraisingAnnouncement
from .forms import ReportForm
from .models import Report


def report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    return render(request, "reports/report_detail.html", {"report": report})


@login_required
def create_report(request, announcement_id):
    announcement = get_object_or_404(FundraisingAnnouncement, pk=announcement_id)
    if announcement.author != request.user:
        return HttpResponseForbidden()

    existing_report = Report.objects.filter(fundraising_announcement=announcement).first()
    if existing_report:
        messages.info(request, "Для цього збору звіт уже створено.")
        return redirect("reports:report", report_id=existing_report.id)

    if not announcement.is_closed:
        messages.warning(request, "Створити звіт можна лише для закритого збору.")
        return redirect("fundraisers:fundraising_announcement", announcement_id=announcement_id)

    if request.method == "GET":
        form = ReportForm()

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.fundraising_announcement = announcement
            obj.save()
            messages.success(request, "Звіт успішно створено.")
            return redirect("reports:report", report_id=obj.id)

    return render(
        request,
        "reports/create_report.html",
        {"form": form, "announcement": announcement},
    )
