import datetime, os
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 
from selenium import webdriver

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
        submit = self.selenium.find_element(By.NAME, "submit")
        submit.click()
        # signout = self.selenium.find_element(By.NAME, "signout")
        # signout.click()
        self.test_profile(email_address, password, git_root_dir)


    def test_profile(self, email_address, password, git_root_dir):
        # editing profile fields
        remove_profile = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "remove_profile")))
        remove_profile.click()
        old_src = self.selenium.find_element(By.CSS_SELECTOR, "img.rounded-circle").get_attribute("src")
        profile_pic = self.selenium.find_element(By.NAME, "profile_pic")
        file_path = os.path.join(git_root_dir, "test2.png")
        profile_pic.send_keys(file_path)
        WebDriverWait(self.selenium, 10).until(
           lambda driver: driver.find_element(By.CSS_SELECTOR, "img.rounded-circle").get_attribute("src") != old_src)
        name_edit = self.selenium.find_element(By.NAME, "name_edit")
        name_edit.click()
        name = self.selenium.find_element(By.NAME, "name")
        name.click()
        name.clear()
        name.send_keys("New Name")
        name_save = self.selenium.find_element(By.NAME, "name_save")
        name_save = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "name_save")))
        name_save.click()
        email_edit = self.selenium.find_element(By.NAME, "email_edit")
        email_edit.click()
        email = self.selenium.find_element(By.NAME, "email")
        email.click()
        email_address = email_address+".uk"
        email.clear()
        email.send_keys(email_address)
        email_check = self.selenium.find_element(By.NAME, "email_check")
        email_check.click()
        email_save = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "email_save")))
        email_save.click()
        password_edit = self.selenium.find_element(By.NAME, "password_edit")
        password_edit.click()
        current_password = self.selenium.find_element(By.NAME, "current_password")
        current_password.click()
        current_password.send_keys(password)
        new_password = self.selenium.find_element(By.NAME, "new_password")
        new_password.click()
        new_pass = password+"1"
        new_password.send_keys(new_pass)
        new_password2 = self.selenium.find_element(By.NAME, "new_password2")
        new_password2.click()
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
        dob_save = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "dob_save")))
        dob_save.click()
        
        # adding hobby
        hobbies = self.selenium.find_element(By.NAME, "hobbies")
        hobbies.click()
        add_hobby = self.selenium.find_element(By.NAME, "add_hobby")
        add_hobby.click()
        hobby_name = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "hobby_name")))
        hobby_name.click()
        hobby_name.send_keys("Baking")
        hobby_description = self.selenium.find_element(By.NAME, "hobby_description")
        hobby_description.click()
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

        # deleting hobby
        delete_hobby = WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "delete_hobby")))
        delete_hobby.click()
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "delete_hobby")))