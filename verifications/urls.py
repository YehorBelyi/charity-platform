from django.urls import path
from .views import VerificationRequestCreateView

urlpatterns = [
    path("create/", VerificationRequestCreateView.as_view(), name="verification_create"),
]
