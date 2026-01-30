from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import VerificationRequestForm
from .models import VerificationDocument


class VerificationRequestCreateView(View):
    template_name = "verifications/verification_form.html"
    success_url = reverse_lazy('verification_status')

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_verified():
            messages.info(request, "Ви вже верифіковані!")
            return redirect(self.success_url)

        if user.verification_requests.filter(status="pending").exists():
            messages.warning(request, "Ви вже відправили запит на перевірку!")
            return redirect(self.success_url)

        form = VerificationRequestForm()

        context = {
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = VerificationRequestForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist("documents")
            if not files:
                form.add_error('documents', 'Будь ласка, завантажте хоча б один файл!')
                return render(request, self.template_name, {'form': form})

            verification_request = form.save(commit=False)
            verification_request.user = request.user
            verification_request.save()

            for f in files:
                VerificationDocument.objects.create(
                    request=verification_request,
                    file=f
                )

            messages.success(request, "Запит надіслано!")
            return redirect(self.success_url)

        messages.error(request, "Виникла помілка під час обробки запиту на верифікацію!")

        context = {"form": form}
        return render(request, self.template_name, context)

class VerificationStatusView(View):
    template_name = "verifications/verification_status.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)