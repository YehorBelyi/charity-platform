from django.contrib import admin
from django.urls import path
from .views import SuccessfulPaymentView, CanceledPaymentView, SetPaymentView, CreateCheckoutSessionView
from .webhooks import stripe_webhook_view

urlpatterns = [
    path('webhooks/stripe/', stripe_webhook_view, name='stripe-webhook'),
    path('success/', SuccessfulPaymentView.as_view(), name='payment-success'),
    path('cancellation/', CanceledPaymentView.as_view(), name='payment-canceled'),
    path('create/<int:announcement_id>', SetPaymentView.as_view(), name='payment-set'),
    path('create-checkout-session/<int:announcement_id>', CreateCheckoutSessionView.as_view(),
         name='create-checkout-session')
]