from decimal import Decimal

from django import forms


class DonationAmountForm(forms.Form):
    """Validate donation amount before redirecting to Stripe."""

    amount = forms.DecimalField(
        label="Сума донату",
        min_value=Decimal("1.00"),
        decimal_places=2,
        max_digits=10,
        error_messages={
            "required": "Вкажіть суму донату.",
            "invalid": "Вкажіть коректну суму донату.",
            "min_value": "Мінімальна сума донату становить 1 грн.",
        },
        widget=forms.NumberInput(
            attrs={
                "class": "donation-modal-input",
                "min": "1",
                "step": "1",
                "placeholder": "Наприклад, 500",
            }
        ),
    )
