from django import forms
from .models import VerificationRequest

class VerificationRequestForm(forms.ModelForm):
    class Meta:
        model = VerificationRequest
        fields = ["requested_role", 'description']