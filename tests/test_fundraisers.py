import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from fundraisers.models import FundraisingAnnouncement
from units.models import Unit

User = get_user_model()


class TestFundraisers:
    @pytest.fixture
    def test_user(self, db):
        return User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
        )

    @pytest.mark.django_db
    def test_create_announcement(self, test_user):
        announcement = FundraisingAnnouncement.objects.create(
            title="Допомога дітям",
            author=test_user,
            target_sum=10000,
            description="Текст опису",
        )

        assert announcement.id is not None
        assert announcement.title == "Допомога дітям"
        assert announcement.author == test_user
        assert announcement.current_sum == 0
        assert announcement.is_closed is False
        assert str(announcement) == "Допомога дітям"

    @pytest.mark.django_db
    def test_announcement_with_unit(self, test_user):
        unit = Unit.objects.create(name="Підрозділ A")

        announcement = FundraisingAnnouncement.objects.create(
            title="Допомога тваринам",
            author=test_user,
            target_sum=5000,
            description="Текст опису",
            unit=unit,
        )

        assert announcement.unit == unit

    @pytest.mark.django_db
    def test_announcement_is_closed_flag(self, test_user):
        announcement = FundraisingAnnouncement.objects.create(
            title="Закрите оголошення",
            author=test_user,
            target_sum=2000,
            description="Текст опису",
            is_closed=True,
        )

        assert announcement.is_closed is True

    @pytest.mark.django_db
    def test_author_can_close_announcement_after_goal_reached(self, client, test_user):
        announcement = FundraisingAnnouncement.objects.create(
            title="Закриття після досягнення цілі",
            author=test_user,
            current_sum=5000,
            target_sum=5000,
            description="Текст опису",
        )
        client.force_login(test_user)

        response = client.post(
            reverse("fundraisers:close_announcement", kwargs={"announcement_id": announcement.id})
        )

        announcement.refresh_from_db()
        assert response.status_code == 302
        assert announcement.is_closed is True

    @pytest.mark.django_db
    def test_author_cannot_close_announcement_before_goal_reached(self, client, test_user):
        announcement = FundraisingAnnouncement.objects.create(
            title="Передчасне закриття",
            author=test_user,
            current_sum=4999,
            target_sum=5000,
            description="Текст опису",
        )
        client.force_login(test_user)

        response = client.post(
            reverse("fundraisers:close_announcement", kwargs={"announcement_id": announcement.id})
        )

        announcement.refresh_from_db()
        assert response.status_code == 302
        assert announcement.is_closed is False
