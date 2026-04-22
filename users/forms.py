"""
Module for forms related to users and their profile information.
"""
from datetime import date

from django import forms
from django.core.validators import RegexValidator

from users.models import CustomUser

import re


#: Regex validator for basic email format verification.
email_validator = RegexValidator(
    regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
    message="Enter a valid email address."
)
# forms.Form

class UserLoginForm(forms.Form):
    """Standard form for user login credentials."""
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'contact-input', 'placeholder':"Ім'я користувача"}), label="Нікнейм")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'contact-input', 'placeholder':'Пароль'}), label="Пароль")



class UserSignUpForm(forms.ModelForm):
    email = forms.EmailField(label="Електронна пошта")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    date_of_birth = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        label="Дата народження"
    )

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name",
                  "email", "password", "phone_number"]
        widgets = {
            'short_bio': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number:
            pattern = r'^\+380\d{9}$'
            if not re.match(pattern, phone_number):
                raise forms.ValidationError("Введіть правильний номер телефону.")

        return phone_number

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Пароль має бути не менше 8 символів.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Пароль повинен містити принаймні 1 цифру.")
        return password

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > date.today():
            raise forms.ValidationError("Дата народження не може бути у майбутньому")
        return date_of_birth


class UserUpdateForm(forms.ModelForm):
    """Form for users to update their personal profile information."""
    # date_of_birth = forms.DateField(
    #     widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    # )

    class Meta:
        model = CustomUser
        # fields = ["avatar", "username", "first_name",
        # "last_name", "status", "rank", "email",
        # "date_of_birth", "phone_number", "short_bio"]
        fields = ["avatar", "first_name", "last_name"]
        widgets = {

            'short_bio': forms.Textarea(attrs={'rows': 4}),
        }
