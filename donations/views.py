"""
This module contains the
views for the donations app.
"""

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from donations.models import Payment
from fundraisers.models import FundraisingAnnouncement
from .services import create_checkout_session


# Create your views here.
class SuccessfulPaymentView(View):
    """View to display the success page after a completed transaction."""
    template_name = 'donations/successful_payment.html'

    def get(self, request):
        """Render the success template."""
        return render(request, self.template_name)

class CanceledPaymentView(View):
    """View to display the cancellation page if the user aborts the payment."""
    template_name = 'donations/canceled_payment.html'

    def get(self, request):
        """Render the cancellation template."""
        return render(request, self.template_name)

class SetPaymentView(View):
    """View to render the initial payment form for a specific announcement."""
    template_name = 'donations/set_payment.html'

    def get(self, request, *args, **kwargs):
        """
        Display the donation form.

        Args:
            announcement_id (int): Passed via URL to identify the fundraising target.
        """
        announcement = get_object_or_404(FundraisingAnnouncement, pk=kwargs.get('announcement_id'))
        context = {'announcement': announcement}
        return render(request, self.template_name, context)

class CreateCheckoutSessionView(View):
    """View to handle the form submission and initiate the Stripe checkout process."""
    def post(self, request, *args, **kwargs):
        """
        Process the donation amount and redirect to Stripe.

        Extracts the amount from the POST data and calls the checkout service.
        In case of failure, logs the error and redirects to the canceled page.
        """
        announcement=get_object_or_404(FundraisingAnnouncement, pk=kwargs.get('announcement_id'))
        amount=request.POST.get('amount')

        try:
            checkout_session = create_checkout_session(announcement=announcement, amount=float(amount))
            return redirect(checkout_session.url)
        except Exception as e:
            logging.error(f"Payment error: {e}")
            request.session['payment_error'] = str(e)
            return redirect('payment-canceled')

class DonationHistoryPartialView(LoginRequiredMixin, View):
    '''
    This class handles requests
    for partial template view.
    '''
    template_name = 'components/donation_history.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        history = Payment.objects.prefetch_related("user").filter(user=current_user).filter(is_finished=True)

        context = {
            'history': history,
        }
        return render(request, self.template_name, context)