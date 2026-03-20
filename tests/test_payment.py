import pytest
from unittest import mock
from django.contrib.auth import get_user_model
from fundraisers.models import FundraisingAnnouncement
from donations.models import Payment


class TestPayment:
    @pytest.fixture
    def user(self):
        User = get_user_model()
        return User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")

    @pytest.fixture
    def announcement(self, user):
        return FundraisingAnnouncement.objects.create(
            title="Допомога тваринам",
            author=user,
            target_sum=1000,
            description="Збір коштів для тварин",
            current_sum=0
        )

    @pytest.mark.django_db
    def test_create_payment(self, announcement):
        payment = Payment.objects.create(
            announcement=announcement,
            amount=100.50,
            stripe_payment_intent="pi_1234567890"
        )

        assert payment.id is not None
        assert payment.amount == 100.50
        assert payment.stripe_payment_intent == "pi_1234567890"
        assert payment.is_finished is False
        assert "❌" in str(payment)


    @pytest.mark.django_db
    def test_mark_payment_finished(self, announcement):
        payment = Payment.objects.create(
            announcement=announcement,
            amount=50.00,
            stripe_payment_intent="pi_abcdef"
        )
        payment.is_finished = True
        payment.save()

        payment.refresh_from_db()
        assert payment.is_finished is True
        assert "✅" in str(payment)

    @pytest.mark.django_db
    def test_create_checkout_session_with_mock(self, announcement):
        with mock.patch("donations.services.stripe.checkout.Session.create") as mock_create:
            mock_create.return_value = mock.Mock(url="https://stripe.com/mock_checkout")

            from donations.services import create_checkout_session
            session = create_checkout_session(announcement, amount=123.45)

            assert session.url == "https://stripe.com/mock_checkout"
            mock_create.assert_called_once()
            args, kwargs = mock_create.call_args
            assert kwargs["payment_method_types"] == ["card"]
            assert kwargs["line_items"][0]["price_data"]["unit_amount"] == int(123.45 * 100)
            assert kwargs["metadata"]["announcement_id"] == announcement.id
