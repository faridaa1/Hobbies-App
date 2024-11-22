import datetime
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class PasswordField(forms.CharField):
    """Password field for Django form - uses type password"""
    widget = forms.PasswordInput


class DatePickerField(forms.DateField):
    """Date field for Djano form with a date picker input"""
    widget = forms.widgets.DateInput(attrs={'type': 'date'})


class SignupForm(ModelForm):
    """Django form used to sign up a user."""
    class Meta:
        """Form based on CustomUser model and has specified fields from that model"""
        model = CustomUser
        fields = ['name', 'email', 'password',
                  'date_of_birth', 'profile_picture']
        field_classes = {
            "password": PasswordField,
            "date_of_birth": DatePickerField
        }
        labels = {
            'name': 'Full Name',
            'profile_picture': 'Profile picture (*.png)'
        }

    def __init__(self, *args, **kwargs):
        """Overriding form constructor"""
        super(SignupForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control',  # For bootstrap styling
                 'placeholder': field}  # Allows bootstrap form animation
            )

    def clean_email(self):
        """Cleans email field - checks that there's no user with that email"""
        email = self.cleaned_data['email']
        email_exists = CustomUser.objects.filter(email=email).exists()
        if email_exists:
            raise ValidationError('An account with that email already exists')
        return email

    def clean_password(self):
        """Cleans password field - checks that password is between 8 and 30 chars"""
        password = self.cleaned_data['password']
        if len(password) < 8 or len(password) > 30:
            raise ValidationError(
                "Your password must be between 8 and 30 characters")
        return password

    def clean_date_of_birth(self):
        """Cleans d.o.b. field - checks that it's not in the future"""
        dob = self.cleaned_data['date_of_birth']
        if dob is None:
            raise ValidationError("You must enter a birthday")
        elif dob > datetime.date.today():
            raise ValidationError("Your birthday cannot be past today")
        return dob

    def clean_profile_picture(self):
        """Cleans profile picture field - checks that it's a png"""
        pic = self.cleaned_data['profile_picture']
        if pic:
            if pic.image.format != 'PNG':
                raise ValidationError('You can only upload .png files')
        return pic
