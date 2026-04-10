from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.forms import ModelForm
from django import forms
from reports.models import Report


class ReportForm(ModelForm):
    donation_document = forms.FileField(label="Акт приймання-передачі благодійної допомоги або інший документ", required=False)
    photo = forms.ImageField(label="Фотозвіт", required=False)
    description = forms.CharField(label="Опис", widget=forms.Textarea())
    spent_sum = forms.DecimalField(label="Витрачені кошти", min_value=1, max_digits=12, decimal_places=2)


    def __init__(self, *args, **kwargs):
        """Configure the FormHelper for crispy-forms."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "my-4 w-100"

        self.helper.layout = Layout(
            Field("donation_document"),
            Field("photo"),
            Field("description", placeholder="Опис"),
            Field("spent_sum", placeholder="Витрачені кошти"),
            Submit("", "Створити звіт")
        )

    class Meta:
        model = Report
        fields = ["donation_document", "photo", "description", "spent_sum"]
