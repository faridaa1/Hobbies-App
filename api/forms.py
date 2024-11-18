import datetime
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class PasswordField(forms.CharField):
    """Password field for Django form"""
    widget = forms.PasswordInput


class DatePickerField(forms.DateField):
    """Date field for Djano form with a date picker input"""
    widget = forms.widgets.DateInput(attrs={'type': 'date'})


class SignupForm(ModelForm):
    """Django form used to sign up a user."""
    class Meta:
        """Form is based on CustomUser model and has following fields"""
        model = CustomUser
        fields = ['username', 'name', 'email', 'password', 'date_of_birth']
        field_classes = {
            "password": PasswordField,
            "date_of_birth": DatePickerField
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        username_exists = CustomUser.objects.filter(username=username).exists()
        if username_exists:
            raise ValidationError(
                "An account with that username already exists")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8 or len(password) > 30:
            raise ValidationError(
                "Your password must be between 8 and 30 characters")
        return password

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        if dob > datetime.date.today():
            raise ValidationError("Your birthday cannot be past today")
        return dob
