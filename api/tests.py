import datetime, os
import django
from django.test import TestCase
from .forms import SignupForm
from .models import CustomUser
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 
from selenium.webdriver.common.keys import Keys

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


class ProfileSeleniumTests(StaticLiveServerTestCase):
    port = 8000

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    # @classmethod 
    # def tearDownClass(cls):
    #     cls.selenium.quit()
    #     super().tearDownClass()
    
    def test_signup(self):
        password = "testing123"
        email_address = "test2231@gmail.com"
        name = "testing"
        self.selenium.get(f"{self.live_server_url}/signup")
        full_name = self.selenium.find_element(By.NAME, "name")
        full_name.send_keys(name)
        email = self.selenium.find_element(By.NAME, "email")
        email.send_keys(email_address)
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys(password)
        date_of_birth = self.selenium.find_element(By.NAME, "date_of_birth")
        date_of_birth.send_keys("2004-01-20")
        show_password = self.selenium.find_element(By.NAME, "show-password")
        show_password.click()
        git_root_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(git_root_dir, "test.png")
        profile_picture = self.selenium.find_element(By.NAME, "profile_picture")
        profile_picture.send_keys(file_path)
        file_path = os.path.join(git_root_dir, "test2.png")
        submit = self.selenium.find_element(By.NAME, "submit")
        submit.click()
        self.test_profile(password)
    

    #login here


    def test_profile(self, password):
        name_edit = self.selenium.find_element(By.NAME, "name_edit")
        name_edit.click()
        name = self.selenium.find_element(By.NAME, "name")
        name.clear()
        name.send_keys("New Name")
        name_save = self.selenium.find_element(By.NAME, "name_save")
        name_save.click()
        email_edit = self.selenium.find_element(By.NAME, "email_edit")
        email_edit.click()
        email = self.selenium.find_element(By.NAME, "email")
        email.send_keys(".uk")
        email_check = self.selenium.find_element(By.NAME, "email_check")
        email_check.click()
        email_save = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "email_save")))
        email_save.click()
        password_edit = self.selenium.find_element(By.NAME, "password_edit")
        password_edit.click()
        current_password = self.selenium.find_element(By.NAME, "current_password")
        current_password.send_keys(password)
        new_password = self.selenium.find_element(By.NAME, "new_password")
        new_pass = password+"1"
        new_password.send_keys(new_pass)
        new_password2 = self.selenium.find_element(By.NAME, "new_password2")
        new_password2.send_keys(new_pass)
        password_check = self.selenium.find_element(By.NAME, "password_check")
        password_check.click()
        password_save = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "password_save")))
        password_save.click()
        dob_edit = self.selenium.find_element(By.NAME, "dob_edit")
        dob_edit.click()
        dob = self.selenium.find_element(By.NAME, "dob")
        dob.click()
        dob.send_keys("22-03-2004")
        dob_save = self.selenium.find_element(By.NAME, "dob_save")
        dob_save.click()
        hobbies = self.selenium.find_element(By.NAME, "hobbies")
        hobbies.click()
        add_hobby = self.selenium.find_element(By.NAME, "add_hobby")
        add_hobby.click()
        hobby_name = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "hobby_name")))
        hobby_name.click()
        hobby_name.send_keys("Baking")
        hobby_description = self.selenium.find_element(By.NAME, "hobby_description")
        hobby_description.send_keys("The art of baking things.")
        level = self.selenium.find_element(By.NAME, "level")
        level.click()
        level_option = self.selenium.find_element(By.NAME, "level_option")
        level_option.click()
        hobby_start_date = self.selenium.find_element(By.NAME, "hobby_start_date")
        hobby_start_date.click()
        hobby_start_date.send_keys("10-10-2010")
        check_hobby = self.selenium.find_element(By.NAME, "check_hobby")
        check_hobby.click()
        save_hobby = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "save_hobby")))
        save_hobby.click()













