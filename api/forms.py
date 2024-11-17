from django import forms
# Same validator used by Django for User usernames
from django.contrib.auth.validators import UnicodeUsernameValidator


class PasswordField(forms.CharField):
    """Password field for Django form"""
    widget = forms.PasswordInput

class DatePickerField(forms.DateField):
    """Date field for Djano form with a date picker input"""
    widget = forms.widgets.DateInput(attrs={'type': 'date'})

class SignupForm(forms.Form):
    """Django form used to sign up a user"""
    # This shows an errror on the form itself it the username isn't valid
    # TODO get this to show as popup
    username = forms.CharField(
        label="username",
        max_length=150,
        validators=[UnicodeUsernameValidator()]
        )
    name = forms.CharField(label="name", max_length=150)
    email = forms.EmailField(label="email")
    password = PasswordField(label="password")
    date_of_birth = DatePickerField(label="Date of birth")
    