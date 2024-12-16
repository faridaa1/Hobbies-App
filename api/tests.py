import datetime
from django.test import TestCase
from .forms import SignupForm
from .models import CustomUser
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 

# https://docs.djangoproject.com/en/5.1/intro/tutorial05/

def valid_signup_data() -> dict:
    """Returns a dict of valid data for a Signup Form"""
    return {
        'username': 'test_email@test.com',
        'name': 'test name',
        'email': 'test_email@test.com',
        'password': 'test_password',
        'date_of_birth': datetime.date.today()
    }


class SignupFormTests(TestCase):
    """Tests for Form to signup a user"""
    @classmethod
    def setUpTestData(cls):
        """Shared data for the SignupFormTests tests"""
        cls.valid_data = valid_signup_data()
        cls.file_data = {'profile_picture': SimpleUploadedFile(
            'test.png', b'file data', content_type='image/png')}

    def test_valid_details(self):
        """Tests that passing valid data to a form is deemed valid"""
        form = SignupForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_email_already_used(self):
        """Tests that an error is raised
        if an account with the given email already exists
        """
        email = 'same@email.com'
        CustomUser.objects.create(username='duplicate_user', email=email, name=email, date_of_birth=self.valid_data['date_of_birth'])
        data = self.valid_data
        data['email'] = email
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [
                         'An account with that email already exists'])

    def test_no_birthday(self):
        """Tests that an error is rasied if no birthday is passed to the form"""
        data = self.valid_data
        del data['date_of_birth']
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['date_of_birth'], [
                         'This field is required.'])

    def test_birthday_in_future(self):
        """Tests that an error is raised if the birthday is in the future"""
        data = self.valid_data
        date = datetime.date.today() + datetime.timedelta(days=1)
        data['date_of_birth'] = date
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['date_of_birth'], [
                         'Your birthday cannot be past today'])

    def test_password_too_short(self):
        """Tests that an error is raised if the password is too short"""
        data = self.valid_data
        data['password'] = 'a'
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], [
                         'Your password must be between 8 and 30 characters'])

    def test_password_too_long(self):
        """Tests that an error is raised if the password is too long"""
        data = self.valid_data
        data['password'] = '_' * 31  # string of 31 _s
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], [
                         'Your password must be between 8 and 30 characters'])

    def test_picture_upload_invalid(self):
        """TODO: Tests that an error is raised if the image uploaded is not a png"""
        pass
        # data = self.valid_data
        # form = SignupForm(data, self.file_data)
        # self.assertFalse(form.is_valid())
        # self.assertEqual(form.errors['profile_picture'],
        #                  'You can only upload .png files')

    def test_upload_no_profile_picture(self):
        """TODO: Tests that a form submitted without a profile picture is valid"""
        pass


class SignupViewTests(TestCase):
    """Tests for Signup view"""

    def test_uses_correct_template(self):
        """Tests that the Signup view uses
        the correct template and returns a 200 response
        """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/spa/signup.html')

    def test_redirect_successful_signup(self):
        """Tests that after sucessfully signing up
        the client gets redirected and returns a 302 response
        """
        response = self.client.post(
            reverse('signup'), data=valid_signup_data())  # Uses url with name 'signup'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://localhost:5173/profile/')

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class ProfileSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(100)

    # @classmethod
    # def tearDownClass(cls):
    #     cls.selenium.quit()
    #     super.tearDownClass()
    
    def test_signup(self):
        password = "testing123"
        email_address = "test223821@gmail.com"
        self.selenium.get(f"{self.live_server_url}/signup")
        full_name = self.selenium.find_element(By.NAME, "name")
        full_name.send_keys(email_address)
        email = self.selenium.find_element(By.NAME, "email")
        email.send_keys(email_address)
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys(password)
        date_of_birth = self.selenium.find_element(By.NAME, "date_of_birth")
        date_of_birth.send_keys("2004-01-20")
        show_password = self.selenium.find_element(By.NAME, "show-password")
        show_password.click()
        profile_picture = self.selenium.find_element(By.NAME, "profile_picture")
        profile_picture.send_keys("C:\\Users\\Farida Uni\\Downloads\\download.png")
        remove_upload_pic = self.selenium.find_element(By.NAME, "remove-upload-pic")
        remove_upload_pic.click()
        profile_picture.send_keys("C:\\Users\\Farida Uni\\Downloads\\flower.png")
        remove_upload_pic.click()
        submit = self.selenium.find_element(By.NAME, "submit")
        submit.click()
        self.test_profile(email_address)
    
    def test_profile(self, email_address):
        name_edit_button = self.selenium.find_element(By.NAME, "name_edit_button")
        name_edit_button.click()
        name = self.selenium.find_element(By.NAME, "name")
        name.send_keys("New Name")
        name_save_button = self.selenium.find_element(By.NAME, "name_save_button")
        name_save_button.click()
