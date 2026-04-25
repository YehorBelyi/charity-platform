"""
This module contains the
views for the donations app.
"""

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from .forms import DonationAmountForm
from donations.models import Payment
from fundraisers.models import FundraisingAnnouncement
from .services import create_checkout_session


# Create your views here.
class SetPaymentView(View):
    """Render donation form content for the announcement modal."""
    template_name = 'donations/set_payment.html'

    def get(self, request, *args, **kwargs):
        """
        Display the donation form.

        Args:
            announcement_id (int): Passed via URL to identify the fundraising target.
        """
        announcement = get_object_or_404(FundraisingAnnouncement, pk=kwargs.get('announcement_id'))
        if request.headers.get("HX-Request") != "true":
            return redirect("fundraisers:fundraising_announcement", announcement_id=announcement.id)

        if announcement.is_closed:
            return render(
                request,
                "donations/set_payment.html",
                {"announcement": announcement, "form": None},
                status=409,
            )

        context = {
            'announcement': announcement,
            'form': DonationAmountForm(),
        }
        return render(request, self.template_name, context)

class CreateCheckoutSessionView(View):
    """View to handle the form submission and initiate the Stripe checkout process."""
    def post(self, request, *args, **kwargs):
        """
        Process the donation amount and redirect to Stripe.

        Extracts the amount from the POST data and calls the checkout service.
        In case of failure, logs the error and returns the form with errors.
        """
        announcement = get_object_or_404(
            FundraisingAnnouncement,
            pk=kwargs.get('announcement_id')
        )
        is_htmx = request.headers.get("HX-Request") == "true"

        if announcement.is_closed:
            if is_htmx:
                return render(
                    request,
                    "donations/set_payment.html",
                    {"announcement": announcement, "form": None},
                    status=409,
                )
            messages.error(request, "Цей збір уже закрито для нових донатів.")
            return redirect("fundraisers:fundraising_announcement", announcement_id=announcement.id)

        form = DonationAmountForm(request.POST)

        if not form.is_valid():
            if is_htmx:
                return render(
                    request,
                    "donations/set_payment.html",
                    {"announcement": announcement, "form": form},
                    status=400,
                )

            messages.error(request, "Вкажіть коректну суму донату.")
            return redirect("fundraisers:fundraising_announcement", announcement_id=announcement.id)

        amount = form.cleaned_data["amount"]

        try:
            checkout_session = create_checkout_session(
                announcement=announcement,
                amount=amount,
                user=request.user if request.user.is_authenticated else None,
            )

            if is_htmx:
                response = HttpResponse(status=204)
                response["HX-Redirect"] = checkout_session.url
                return response

            return redirect(checkout_session.url)
        except Exception as e:
            logging.error(f"Payment error: {e}")
            form.add_error(None, "Не вдалося підготувати оплату. Спробуйте ще раз.")

            if is_htmx:
                return render(
                    request,
                    "donations/set_payment.html",
                    {"announcement": announcement, "form": form},
                    status=400,
                )

            messages.error(request, "Не вдалося підготувати оплату. Спробуйте ще раз.")
            return redirect("fundraisers:fundraising_announcement", announcement_id=announcement.id)

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
