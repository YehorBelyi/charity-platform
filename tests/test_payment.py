from decimal import Decimal
from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from donations.models import Payment
from fundraisers.models import FundraisingAnnouncement


class TestPayment:
    @pytest.fixture
    def user(self):
        User = get_user_model()
        return User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )

    @pytest.fixture
    def announcement(self, user):
        return FundraisingAnnouncement.objects.create(
            title="Допомога тваринам",
            author=user,
            target_sum=1000,
            description="Збір коштів для тварин",
            current_sum=0,
        )

    @pytest.mark.django_db
    def test_create_payment(self, announcement):
        payment = Payment.objects.create(
            announcement=announcement,
            amount=Decimal("100.50"),
            stripe_payment_intent="pi_1234567890",
        )

        assert payment.id is not None
        assert payment.amount == Decimal("100.50")
        assert payment.stripe_payment_intent == "pi_1234567890"
        assert payment.is_finished is False

    @pytest.mark.django_db
    def test_mark_payment_finished(self, announcement):
        payment = Payment.objects.create(
            announcement=announcement,
            amount=Decimal("50.00"),
            stripe_payment_intent="pi_abcdef",
        )
        payment.is_finished = True
        payment.save()

        payment.refresh_from_db()
        assert payment.is_finished is True

    @pytest.mark.django_db
    def test_create_checkout_session_with_mock(self, announcement, user):
        with mock.patch("donations.services.stripe.checkout.Session.create") as mock_create:
            mock_create.return_value = mock.Mock(url="https://stripe.com/mock_checkout")

            from donations.services import create_checkout_session

            session = create_checkout_session(
                announcement,
                amount=Decimal("123.45"),
                user=user,
            )

            assert session.url == "https://stripe.com/mock_checkout"
            mock_create.assert_called_once()
            args, kwargs = mock_create.call_args
            assert kwargs["payment_method_types"] == ["card"]
            assert kwargs["line_items"][0]["price_data"]["unit_amount"] == 12345
            assert kwargs["metadata"]["announcement_id"] == announcement.id
            assert kwargs["metadata"]["user_id"] == str(user.id)
            assert "payment_status=success" in kwargs["success_url"]
            assert "payment_status=canceled" in kwargs["cancel_url"]

    @pytest.mark.django_db
    def test_set_payment_redirects_to_announcement_without_htmx(self, client, announcement):
        response = client.get(reverse("payment-set", args=[announcement.id]))

        assert response.status_code == 302
        assert response.url == reverse(
            "fundraisers:fundraising_announcement",
            args=[announcement.id],
        )

    @pytest.mark.django_db
    def test_set_payment_returns_modal_partial_for_htmx(self, client, announcement):
        response = client.get(
            reverse("payment-set", args=[announcement.id]),
            HTTP_HX_REQUEST="true",
        )

        assert response.status_code == 200
        assert "Сума донату" in response.content.decode("utf-8")

    @pytest.mark.django_db
    def test_create_checkout_session_returns_hx_redirect(self, client, announcement, user):
        client.force_login(user)

        with mock.patch("donations.views.create_checkout_session") as mock_checkout:
            mock_checkout.return_value = mock.Mock(url="https://stripe.com/checkout")

            response = client.post(
                reverse("create-checkout-session", args=[announcement.id]),
                data={"amount": "250"},
                HTTP_HX_REQUEST="true",
            )

        assert response.status_code == 204
        assert response.headers["HX-Redirect"] == "https://stripe.com/checkout"
        mock_checkout.assert_called_once()

    @pytest.mark.django_db
    def test_invalid_donation_amount_returns_modal_errors(self, client, announcement):
        response = client.post(
            reverse("create-checkout-session", args=[announcement.id]),
            data={"amount": "0"},
            HTTP_HX_REQUEST="true",
        )

        assert response.status_code == 400
        assert "Мінімальна сума донату становить 1 грн." in response.content.decode("utf-8")

    @pytest.mark.django_db
    def test_webhook_updates_payment_sum_and_user(self, client, announcement, user):
        fake_event = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "metadata": {
                        "announcement_id": str(announcement.id),
                        "amount": "200.00",
                        "user_id": str(user.id),
                    },
                    "payment_intent": "pi_webhook_123",
                }
            },
        }

        with mock.patch("donations.webhooks.stripe.Webhook.construct_event", return_value=fake_event):
            response = client.post(
                reverse("stripe-webhook"),
                data=b"{}",
                content_type="application/json",
                HTTP_STRIPE_SIGNATURE="test-signature",
            )

        assert response.status_code == 200

        announcement.refresh_from_db()
        assert announcement.current_sum == Decimal("200.00")

        payment = Payment.objects.get(stripe_payment_intent="pi_webhook_123")
        assert payment.user == user
        assert payment.is_finished is True

    @pytest.mark.django_db
    def test_announcement_page_shows_payment_status(self, client, announcement):
        response = client.get(
            reverse("fundraisers:fundraising_announcement", args=[announcement.id]),
            {"payment_status": "success", "payment_amount": "300"},
        )

        assert response.status_code == 200
        body = response.content.decode("utf-8")
        assert "Оплату завершено" in body
        assert "300" in body
