import datetime
from django.test import TestCase
from .forms import SignupForm
from .models import CustomUser

# https://docs.djangoproject.com/en/5.1/intro/tutorial05/


class SignupFormTests(TestCase):
    """Tests for Form to signup a user"""
    @classmethod
    def setUpTestData(cls):
        cls.valid_data = {  # All vals are valid - used by test cases checking invalid data
            'username': 'test_username',
            'name': 'test name',
            'email': 'test_email@test.com',
            'password': 'test_password',
            'date_of_birth': datetime.date.today()
        }

    def test_valid_details(self):
        form = SignupForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_username_already_exists(self):
        CustomUser.objects.create(username='duplicate_user')
        data = self.valid_data
        data['username'] = 'duplicate_user'
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

    def test_birthday_in_future(self):
        data = self.valid_data
        date = datetime.date.today() + datetime.timedelta(days=1)
        data['date_of_birth'] = date
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_password_length(self):
        data = self.valid_data
        data['password'] = ''
        data['password'] = '_' * 31  # string of 31 _s
        form = SignupForm(data=data)
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
