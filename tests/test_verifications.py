import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from verifications.models import VerificationRequest


User = get_user_model()


@pytest.mark.django_db
class TestVerificationFlow:
    def test_unverified_user_is_redirected_from_create_fundraiser(self, client):
        user = User.objects.create_user(
            username="creator",
            email="creator@example.com",
            password="password123",
        )
        client.force_login(user)

        response = client.get(reverse("fundraisers:create_announcement"))

        assert response.status_code == 302
        assert response.url == reverse("verification_create")

    def test_verified_user_can_open_create_fundraiser_page(self, client):
        user = User.objects.create_user(
            username="verified_creator",
            email="verified_creator@example.com",
            password="password123",
        )
        VerificationRequest.objects.create(
            user=user,
            requested_role=VerificationRequest.Role.VOLUNTEER,
            status=VerificationRequest.Status.APPROVED,
        )
        client.force_login(user)

        response = client.get(reverse("fundraisers:create_announcement"))

        assert response.status_code == 200

    def test_verification_page_requires_login(self, client):
        response = client.get(reverse("verification_create"))

        assert response.status_code == 302
        assert reverse("login") in response.url

    def test_pending_request_cannot_be_duplicated(self, client):
        user = User.objects.create_user(
            username="pending_user",
            email="pending@example.com",
            password="password123",
        )
        VerificationRequest.objects.create(
            user=user,
            requested_role=VerificationRequest.Role.MILITARY,
            status=VerificationRequest.Status.PENDING,
        )
        client.force_login(user)

        upload = SimpleUploadedFile(
            "doc.txt",
            b"verification document",
            content_type="text/plain",
        )

        response = client.post(
            reverse("verification_create"),
            data={
                "requested_role": VerificationRequest.Role.VOLUNTEER,
                "description": "Ще одна спроба",
                "documents": [upload],
            },
        )

        assert response.status_code == 200
        assert VerificationRequest.objects.filter(user=user).count() == 1
