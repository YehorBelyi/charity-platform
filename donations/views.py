import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View

from donations.models import Payment
from fundraisers.models import FundraisingAnnouncement
from .services import create_checkout_session


# Create your views here.
class SuccessfulPaymentView(View):
    template_name = 'donations/successful_payment.html'

    def get(self, request):
        return render(request, self.template_name)

class CanceledPaymentView(View):
    template_name = 'donations/canceled_payment.html'

    def get(self, request):
        return render(request, self.template_name)

class SetPaymentView(View):
    template_name = 'donations/set_payment.html'

    def get(self, request, *args, **kwargs):
        announcement = get_object_or_404(FundraisingAnnouncement, pk=kwargs.get('announcement_id'))
        context = {'announcement': announcement}
        return render(request, self.template_name, context)

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        announcement=get_object_or_404(FundraisingAnnouncement, pk=kwargs.get('announcement_id'))
        amount=request.POST.get('amount')

        try:
            checkout_session = create_checkout_session(announcement=announcement, amount=float(amount))
            return redirect(checkout_session.url)
        except Exception as e:
            print(e)
            logging.error(f"Payment error: {e}")
            request.session['payment_error'] = str(e)
            return redirect('payment-canceled')