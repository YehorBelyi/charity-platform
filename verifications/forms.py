from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from .models import VerificationRequest, VerificationDocument

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import VerificationRequest

class VerificationRequestForm(forms.ModelForm):
    documents = forms.FileField(
        label="Документи",
        widget=forms.ClearableFileInput(),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['documents'].widget.attrs.update({'multiple': True})
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"
        self.helper.layout = Layout(
            Field("requested_role"),
            Field("documents"),
            Field("description"),
            Submit("submit", "Подати заявку", css_class="btn btn-primary w-100 mt-3")
        )

    class Meta:
        model = VerificationRequest
        fields = ["requested_role", 'description']