from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Submit, Layout
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

    def __init__(self, *args, **kwargs):
        """Configure the FormHelper for crispy-forms."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "my-4 w-100"

        self.helper.layout = Layout(
            Field("search", placeholder="Назва збору"),
            Submit("", "Пошук")
        )