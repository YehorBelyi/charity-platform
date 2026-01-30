from django.urls import path
from .views import VerificationRequestCreateView, VerificationStatusView

urlpatterns = [
    path("create/", VerificationRequestCreateView.as_view(), name="verification_create"),
    path("status/", VerificationStatusView.as_view(), name="verification_status"),
]
