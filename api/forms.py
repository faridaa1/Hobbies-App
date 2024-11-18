from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
# Same validator used by Django for User usernames
from django.contrib.auth.validators import UnicodeUsernameValidator
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
    