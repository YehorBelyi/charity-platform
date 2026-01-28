from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Submit, Layout
from django import forms
from .models import FundraisingAnnouncement

class AddFundraisingAnnouncementForm(forms.ModelForm):
    title = forms.CharField(label="Назва збору:")
    target_sum = forms.DecimalField(label="Ціль (ГРН):", min_value=0.01)
    description = forms.CharField(label="Опис:", widget=forms.Textarea())
    photo = forms.ImageField(label="Фото для збору:", required=False)
    operational_direction = forms.CharField(label="Напрямок фронту:", required=False)
    unit = forms.CharField(label="Підрозділ:", required=False)

    def __init__(self, *args, **kwargs):
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
            Submit("submit", "Створити збір")
        )

    class Meta:
        model = FundraisingAnnouncement
        fields = ("title", "target_sum", "description", "photo", "operational_direction", "unit")
