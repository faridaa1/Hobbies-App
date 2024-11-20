import datetime
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class PasswordField(forms.CharField):
    """Password field for Django form - uses type password"""
    widget = forms.PasswordInput(attrs={'minlength': '8', 'maxlength': '30'})


class DatePickerField(forms.DateField):
    """Date field for Djano form with a date picker input"""
    widget = forms.widgets.DateInput(attrs={'type': 'date'})


class SignupForm(ModelForm):
    """Django form used to sign up a user."""
    confirm_password = PasswordField(label='Confirm Password')
    field_order = ['name', 'email', 'password',
                   'confirm_password', 'date_of_birth', 'profile_picture']

    class Meta:
        """Form is based on CustomUser model
        and has following fields from that model
        """
        model = CustomUser
        fields = ['name', 'email', 'password',
                  'date_of_birth', 'profile_picture']
        field_classes = {
            "password": PasswordField,
            "date_of_birth": DatePickerField
        }
        labels = {
            'name': 'Full Name',
            'profile_picture': 'Profile picture (*.png)',
        }

    def __init__(self, *args, **kwargs):
        """Overriding form constructor"""
        super(SignupForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control',  # For bootstrap styling
                 'placeholder': self.fields[field].label}  # Placeholder is same as input label
            )

    def clean_email(self):
        """Validate that there isn't already an account with the same email"""
        email = self.cleaned_data['email']
        email_exists = CustomUser.objects.filter(email=email).exists()
        if email_exists:
            raise ValidationError('An account with that email already exists')
        return email

    def clean_password(self):
        """Validate password length is between 8 and 30 inclusive"""
        password = self.cleaned_data['password']
        if len(password) < 8 or len(password) > 30:
            raise ValidationError(
                "Your password must be between 8 and 30 characters")
        return password

    def clean_date_of_birth(self):
        """Validate that the date of birth is not in the future"""
        dob = self.cleaned_data['date_of_birth']
        if dob is None:
            raise ValidationError("You must enter a birthday")
        elif dob > datetime.date.today():
            raise ValidationError("Your birthday cannot be past today")
        return dob

    def clean_profile_picture(self):
        """Validate that the image uploaded is a .png"""
        pic = self.cleaned_data['profile_picture']
        if pic:
            if pic.image.format != 'PNG':
                raise ValidationError('You can only upload .png files')
        return pic

    def clean(self):
        """Validation of the form which needs multiple form fields"""
        cleaned_data = super().clean()  # Keeps validation
        password = cleaned_data.get('password')
        confirm_password = cleaned_data['confirm_password']

        # If both password fields are valid
        if confirm_password and password:
            if confirm_password != password:
                self.add_error('password', 'Passwords do not match')
                self.add_error('confirm_password', 'Passwords do not match')
