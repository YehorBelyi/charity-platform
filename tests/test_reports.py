import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from fundraisers.models import FundraisingAnnouncement
from reports.models import Report

User = get_user_model()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username="reportuser",
        email="report@example.com",
        password="password123",
    )


@pytest.mark.django_db
def test_author_can_create_report_for_closed_announcement(client, test_user):
    announcement = FundraisingAnnouncement.objects.create(
        title="Закритий збір",
        author=test_user,
        current_sum=12000,
        target_sum=10000,
        description="Опис збору",
        is_closed=True,
    )
    client.force_login(test_user)

    response = client.post(
        reverse("reports:create", kwargs={"announcement_id": announcement.id}),
        data={
            "description": "Кошти використано на закупівлю спорядження.",
            "spent_sum": "9500.00",
            "donation_document": SimpleUploadedFile(
                "report.txt",
                b"report evidence",
                content_type="text/plain",
            ),
        },
    )

    report = Report.objects.get(fundraising_announcement=announcement)
    assert response.status_code == 302
    assert report.description == "Кошти використано на закупівлю спорядження."


@pytest.mark.django_db
def test_author_cannot_create_report_for_open_announcement(client, test_user):
    announcement = FundraisingAnnouncement.objects.create(
        title="Відкритий збір",
        author=test_user,
        current_sum=4000,
        target_sum=10000,
        description="Опис збору",
        is_closed=False,
    )
    client.force_login(test_user)

    response = client.post(
        reverse("reports:create", kwargs={"announcement_id": announcement.id}),
        data={
            "description": "Спроба створити звіт зарано.",
            "spent_sum": "3000.00",
        },
    )

    assert response.status_code == 302
    assert Report.objects.filter(fundraising_announcement=announcement).count() == 0


@pytest.mark.django_db
def test_second_report_redirects_to_existing_one(client, test_user):
    announcement = FundraisingAnnouncement.objects.create(
        title="Закритий збір зі звітом",
        author=test_user,
        current_sum=8000,
        target_sum=8000,
        description="Опис збору",
        is_closed=True,
    )
    existing_report = Report.objects.create(
        fundraising_announcement=announcement,
        description="Перший звіт",
        spent_sum="7800.00",
    )
    client.force_login(test_user)

    response = client.get(
        reverse("reports:create", kwargs={"announcement_id": announcement.id})
    )

    assert response.status_code == 302
    assert response.url == reverse("reports:report", kwargs={"report_id": existing_report.id})
