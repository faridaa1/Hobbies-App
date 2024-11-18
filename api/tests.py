import datetime
from django.test import TestCase
from .forms import SignupForm
from .models import CustomUser

# https://docs.djangoproject.com/en/5.1/intro/tutorial05/


class SignupFormTests(TestCase):
    """Tests for Form to signup a user"""

    def test_birthday_in_future(self):
        date = datetime.date.today() + datetime.timedelta(days=1) # 1 day in future
        form = SignupForm(data={'date_of_birth': date})
        self.assertFalse(form.is_valid())


class SignupViewTests(TestCase):
    """Tests for Signup view"""
    def setUp(self):
        # CustomUser.objects.create()
        pass

    def test_username_already_used(self):
        pass
    
    def test_email_already_used(self):
        pass

    def test_uses_correct_template(self):
        pass

    def test_redirect_successful_signup(self):
        pass