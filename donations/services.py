import stripe
from django.conf import settings
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(announcement, amount):
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
            "amount": amount
        },
        success_url=settings.DOMAIN + reverse('payment-success'),
        cancel_url=settings.DOMAIN + reverse('payment-canceled'),
    )
    return session