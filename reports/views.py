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

    if request.method == "GET":
        form = ReportForm()

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.fundraising_announcement = announcement
            obj.save()
            return redirect("fundraisers:fundraising_announcement", announcement_id=announcement_id)

    return render(request, "reports/create_report.html", {"form": form})
