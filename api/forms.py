from django import forms


class PasswordField(forms.CharField):
    """Password field for Django form"""
    widget = forms.PasswordInput

class DatePickerField(forms.DateField):
    """Date field for Djano form with a date picker input"""
    widget = forms.widgets.DateInput(attrs={'type': 'date'})

class SignupForm(forms.Form):
    """Django form used to sign up a user"""
    name = forms.CharField(label="name", max_length=150)
    email = forms.EmailField(label="email")
    passowrd = PasswordField(label="password")
    date_of_birth = DatePickerField(label="Date of birth")
    