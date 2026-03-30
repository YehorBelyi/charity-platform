"""
This module contains webhooks,
which handles all payment processes
on the website.
"""

import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from fundraisers.models import FundraisingAnnouncement
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

@csrf_exempt
def stripe_webhook_view(request):
    """
    Handle Stripe webhook events to process asynchronous payment updates.

    This view verifies the Stripe signature, constructs the event, and
    if the payment is successful (checkout.session.completed), it creates
    a corresponding Payment record in the database.

    Args:
        request (HttpRequest): The incoming POST request from Stripe.

    Returns:
        HttpResponse: 200 OK if processed, 400 Bad Request on verification failure.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        announcement_id = session["metadata"]["announcement_id"]
        amount = session["metadata"]["amount"]

        announcement = FundraisingAnnouncement.objects.get(
            id=announcement_id
        )

        Payment.objects.create(
            announcement=announcement,
            amount=amount,
            stripe_payment_intent=session["payment_intent"],
            is_finished=True
        )

    return HttpResponse(status=200)
