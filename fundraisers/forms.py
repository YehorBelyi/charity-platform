"""Forms for the fundraisers app"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Submit, Layout, Div, HTML
from django import forms
from units.models import Unit
from .models import FundraisingAnnouncement

class AddUpdateFundraisingAnnouncementForm(forms.ModelForm):
    """Form for creating announcements."""

    #: Announcement title.
    title = forms.CharField(label="Назва збору:")
    #: Amount needed to reach the fundraising goal.
    target_sum = forms.DecimalField(label="Ціль (ГРН):", min_value=0.01)
    #: Main information about announcement.
    description = forms.CharField(label="Опис:", widget=forms.Textarea())
    #: Photo representing the announcement.
    photo = forms.ImageField(label="Фото для збору:", required=False)
    #: The operational direction where the supported unit is deployed.
    operational_direction = forms.CharField(label="Напрямок фронту:", required=False)
    #: Supported unit.
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), label="Підрозділ", required=False)

    def __init__(self, *args, **kwargs):
        """Configure the FormHelper for crispy-forms."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "mt-5"

        self.helper.layout = Layout(
            Field("title"),
            Field("target_sum"),
            Field("description"),
            Field("unit"),
            Field("operational_direction"),
            Field("photo"),
            Submit("submit", "Відправити")
        )

    class Meta:
        model = FundraisingAnnouncement
        fields = ("title", "target_sum", "description", "photo", "operational_direction", "unit")


class SearchForm(forms.Form):
    """Form for searching announcements."""

    #: Search query.
    search = forms.CharField(max_length=300, required=False, label="")
    #: Select field for ordering fundraising announcements.
    ordering = forms.ChoiceField(choices=[
        ("popular", "Найбільш популярні"), ("newest", "Найновіші"), ("biggest", "Найбільші")
    ], required=False, label="")

    def __init__(self, *args, **kwargs):
        """Configure the FormHelper for crispy-forms."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "w-100"

        self.helper.layout = Layout(
            Div(
                Div(
                    Field("search", placeholder="Назва збору", css_class="search-input", wrapper_class="mt-3"),
                    css_class="flex-grow-1",
                ),

                HTML("""
                    <button type="submit" class="search-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                          <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                        </svg>               
                    </button>
                    """),
                css_class="d-flex gap-2"
            ),

            Div(
            Field("ordering", wrapper_class="mt-3", onchange="this.form.submit()", css_class="ordering-select"),
                css_class="ordering-select-container",
            )
        )
