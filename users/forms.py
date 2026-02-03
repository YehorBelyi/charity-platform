from django import forms
from django.core.validators import RegexValidator

from users.models import CustomUser

email_validator = RegexValidator(
    regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
    message="Enter a valid email address."
)
# forms.Form

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)


class UserSignUpForm(forms.ModelForm):
    email = forms.EmailField(validators=[email_validator])
    password = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "password", "date_of_birth", "phone_number", "gender"]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number']