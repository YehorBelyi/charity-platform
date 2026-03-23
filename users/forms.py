from django import forms
from django.core.validators import RegexValidator

from users.models import CustomUser

#: Regex validator for basic email format verification.
email_validator = RegexValidator(
    regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
    message="Enter a valid email address."
)
# forms.Form

class UserLoginForm(forms.Form):
    """Standard form for user login credentials."""
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)


class UserSignUpForm(forms.ModelForm):
    """Form for registering a new CustomUser with detailed profile data."""
    email = forms.EmailField(validators=[email_validator])
    password = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "status", "rank",
                  "email", "password", "date_of_birth", "phone_number", "short_bio"]
        widgets = {
            'short_bio': forms.Textarea(attrs={'rows': 4}),
        }


class UserUpdateForm(forms.ModelForm):
    """Form for users to update their personal profile information."""
    # date_of_birth = forms.DateField(
    #     widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    # )

    class Meta:
        model = CustomUser
        # fields = ["avatar", "username", "first_name", "last_name", "status", "rank", "email", "date_of_birth", "phone_number", "short_bio"]
        fields = ["avatar", "first_name", "last_name"]
        widgets = {

            'short_bio': forms.Textarea(attrs={'rows': 4}),
        }