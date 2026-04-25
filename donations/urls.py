"""
URL configuration for the donations application.

This module defines view routes for:\n
- Stripe Webhook integration.\n
- Donation session creation and forms.
"""

from django.urls import path
from .views import SetPaymentView, CreateCheckoutSessionView, DonationHistoryPartialView
from .webhooks import stripe_webhook_view

urlpatterns = [
    #: Stripe webhook endpoint for processing payment events.
    path('webhooks/stripe/', stripe_webhook_view, name='stripe-webhook'),
    #: Initial page to set donation amount for a specific announcement.
    path('create/<int:announcement_id>', SetPaymentView.as_view(), name='payment-set'),
    #: Action endpoint to create a Stripe Checkout Session.
    path('create-checkout-session/<int:announcement_id>', CreateCheckoutSessionView.as_view(),
         name='create-checkout-session'),
    #: Partial view for donation history.
    path('history/', DonationHistoryPartialView.as_view(), name='donation-history'),
]
