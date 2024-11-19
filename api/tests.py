import datetime
from django.test import TestCase
from .forms import SignupForm
from .models import CustomUser
from django.urls import reverse

# https://docs.djangoproject.com/en/5.1/intro/tutorial05/


def valid_signup_data() -> dict:
    """Returns a dict of valid data for a Signup Form"""
    return {
        'username': 'test_username',
        'name': 'test name',
        'email': 'test_email@test.com',
        'password': 'test_password',
        'date_of_birth': datetime.date.today()
    }


class SignupFormTests(TestCase):
    """Tests for Form to signup a user"""
    @classmethod
    def setUpTestData(cls):
        cls.valid_data = valid_signup_data()

    def test_valid_details(self):
        form = SignupForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_username_already_exists(self):
        username = 'duplicate_user'
        CustomUser.objects.create(username=username)
        data = self.valid_data
        data['username'] = username
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [
                         'An account with that username already exists'])

    def test_email_already_used(self):
        email = 'same@email.com'
        CustomUser.objects.create(username='duplicate_user', email=email)
        data = self.valid_data
        data['email'] = email
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [
                         'An account with that email already exists'])

    def test_birthday_in_future(self):
        data = self.valid_data
        date = datetime.date.today() + datetime.timedelta(days=1)
        data['date_of_birth'] = date
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['date_of_birth'], [
                         'Your birthday cannot be past today'])

    def test_password_too_short(self):
        data = self.valid_data
        data['password'] = 'a'
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], [
                         'Your password must be between 8 and 30 characters'])

    def test_password_too_long(self):
        data = self.valid_data
        data['password'] = '_' * 31  # string of 31 _s
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], [
                         'Your password must be between 8 and 30 characters'])

    def test_picture_upload(self):
        self.assertEqual(1, 2)


class SignupViewTests(TestCase):
    """Tests for Signup view"""

    def setUp(self):
        pass

    def test_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/spa/signup.html')

    def test_redirect_successful_signup(self):
        response = self.client.post(
            reverse('signup'), data=valid_signup_data())  # Uses url with name 'signup'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
