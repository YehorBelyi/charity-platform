from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse

from .forms import VerificationRequestForm
from .models import VerificationDocument


class VerificationRequestCreateView(View):
    template_name = "verifications/verification_form.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        is_form_shown = True

        last_request = user.verification_requests.order_by("-created_at").first()

        if user.is_verified():
            messages.info(request, "Ви вже верифіковані!")
            is_form_shown = False
        elif last_request:
            if last_request.status == "pending":
                messages.warning(request, "Ви вже відправили запит на перевірку!")
                is_form_shown = False
            elif last_request.status == "rejected":
                messages.error(request, "На жаль, ваш запит на верифікацію відхилено. Спробуйте ще раз!")
                is_form_shown = True

        form = VerificationRequestForm()

        context = {
            "form": form,
            "is_form_shown": is_form_shown,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = VerificationRequestForm(request.POST)
        files = request.FILES.getlist("documents")

        if len(files) > 3:
            messages.error(request, "Можна прикріпити до 3 документів!")
            return render(request, self.template_name, {"form": form, "is_form_shown": True})

        if not files:
            messages.error(request, 'Будь ласка, завантажте хоча б один файл!')
            return render(request, self.template_name, {'form': form, "is_form_shown": True})

        if form.is_valid():
            verification_request = form.save(commit=False)
            verification_request.user = request.user
            verification_request.save()

            for f in files:
                VerificationDocument.objects.create(
                    request=verification_request,
                    file=f
                )

            messages.success(request, "Запит надіслано!")
            return render(request, self.template_name, {'form': form, "is_form_shown": False})

        messages.error(request, "Виникла помілка під час обробки запиту на верифікацію!")

        context = {"form": form, "show_form": True}
        return render(request, self.template_name, context)