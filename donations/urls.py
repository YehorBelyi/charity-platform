"""
URL configuration for the donations application.

This module defines view routes for:\n
- Stripe Webhook integration.\n
- Payment success and cancellation pages.\n
- Donation session creation and forms.
"""

from django.contrib import admin
from django.urls import path
from .views import SuccessfulPaymentView, CanceledPaymentView, SetPaymentView, CreateCheckoutSessionView
from .webhooks import stripe_webhook_view

urlpatterns = [
    #: Stripe webhook endpoint for processing payment events.
    path('webhooks/stripe/', stripe_webhook_view, name='stripe-webhook'),
    #: Redirect page for successful payments.
    path('success/', SuccessfulPaymentView.as_view(), name='payment-success'),
    #: Redirect page for canceled or failed payments.
    path('cancellation/', CanceledPaymentView.as_view(), name='payment-canceled'),
    #: Initial page to set donation amount for a specific announcement.
    path('create/<int:announcement_id>', SetPaymentView.as_view(), name='payment-set'),
    #: Action endpoint to create a Stripe Checkout Session.
    path('create-checkout-session/<int:announcement_id>', CreateCheckoutSessionView.as_view(),
         name='create-checkout-session')
]