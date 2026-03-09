import stripe
from django.conf import settings
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(announcement, amount):
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