import stripe
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(announcement, amount, user=None):
    """
    Create a Stripe Checkout Session for a donation.

    This service prepares the line items, currency (UAH), and metadata
    required for Stripe to process the payment and redirect the user back.

    Args:
        announcement (FundraisingAnnouncement): The announcement object being funded.
        amount (float): The donation amount.

    Returns:
        stripe.checkout.Session: The created Stripe session object containing the redirect URL.
    """
    success_query = urlencode({
        "payment_status": "success",
        "payment_amount": str(amount),
    })
    cancel_query = urlencode({
        "payment_status": "canceled",
    })

    success_url = (
        settings.DOMAIN
        + reverse("fundraisers:fundraising_announcement", kwargs={"announcement_id": announcement.id})
        + f"?{success_query}"
    )
    cancel_url = (
        settings.DOMAIN
        + reverse("fundraisers:fundraising_announcement", kwargs={"announcement_id": announcement.id})
        + f"?{cancel_query}"
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            'price_data': {
                'currency': 'uah',
                'product_data': {
                    'name': announcement.title,
                },
                'unit_amount': int(amount * 100),
            },
            'quantity': 1,
        }],
        mode="payment",
        metadata={
            "announcement_id": announcement.id,
            "amount": str(amount),
            "user_id": str(user.id) if user and user.is_authenticated else "",
        },
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session
