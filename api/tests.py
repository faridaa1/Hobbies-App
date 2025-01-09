import datetime, os, json
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 
from api.models import CustomUser

# https://docs.djangoproject.com/en/5.1/intro/tutorial05/

def valid_signup_data() -> dict:
    """Returns a dict of valid data for a Signup Form"""
    git_root_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(git_root_dir, "test.png")
    file_path2 = os.path.join(git_root_dir, "test2.png")
    return {
        'username': 'test_email@test.com',
        'name': 'test name',
        'email': 'test_email@test.com',
        'password': 'test_password',
        'date_of_birth': datetime.date.today(),
        'file_path': file_path,
        'file_path2': file_path2
    }

import time
class ProfileSeleniumTests(StaticLiveServerTestCase):
    port = 8000
    fixtures = ['users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    # @classmethod 
    # def tearDownClass(cls):
    #     cls.selenium.quit()
    #     super().tearDownClass()
    
    def test_signup(self):
        """Testing account creation / signup"""
        self.selenium.get(f"{self.live_server_url}/signup")
        full_name = self.selenium.find_element(By.NAME, "name")
        full_name.click()
        full_name.send_keys(valid_signup_data()['name'])

        email = self.selenium.find_element(By.NAME, "email")
        email.click()
        email.send_keys(valid_signup_data()['email'])
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.click()
        password_input.send_keys(valid_signup_data()['password'])
        date_of_birth = self.selenium.find_element(By.NAME, "date_of_birth")
        date_of_birth.click()
        date_of_birth.send_keys(valid_signup_data()['date_of_birth'].strftime('%d-%m-%Y'))
        show_password = self.selenium.find_element(By.NAME, "show-password")
        show_password.click()
        profile_picture = self.selenium.find_element(By.NAME, "profile_picture")
        profile_picture.send_keys(valid_signup_data()['file_path'])
        submit = self.selenium.find_element(By.NAME, "submit")
        submit.click()
        self.test_login()
    
    def test_login(self):
        """Testing login"""
        signout = WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "signout")))
        signout.click()
        email = WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "email")))
        email.click()
        email.send_keys(valid_signup_data()['email'])
        password = self.selenium.find_element(By.NAME, "password")
        password.click()
        password.send_keys(valid_signup_data()['password'])
        submit = self.selenium.find_element(By.NAME, "submit")
        submit.click()
        self.test_profile()


    def test_profile(self):
        """Testing editing all the user's data on their profile page"""
        self.test_profile_edit()
    
    def test_profile_edit(self):
        """Testing editing all profile details"""
        remove_profile = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "remove_profile")))
        remove_profile.click()
        old_src = self.selenium.find_element(By.CSS_SELECTOR, "img.rounded-circle").get_attribute("src")
        profile_pic = self.selenium.find_element(By.NAME, "profile_pic")
        profile_pic.send_keys(valid_signup_data()['file_path2'])
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
        email_address = valid_signup_data()['email']+".uk"
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
        current_password.send_keys(valid_signup_data()['password'])
        new_password = self.selenium.find_element(By.NAME, "new_password")
        new_password.click()
        new_pass = valid_signup_data()['password']+"1"
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
        self.test_add_hobby()
        
    def test_add_hobby(self):
        """Testing editing hobbies"""
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
        self.test_send_friend_request()

    def test_send_friend_request(self):
        """Testing sending a friend request"""
        users = self.selenium.find_element(By.LINK_TEXT, "Users")
        users.click()
        send_request = WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "send-request")))
        send_request.click()
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "status")))
        self.test_accept_friend_request()

    def test_accept_friend_request(self):
        """Testing login as the other user and accept the freind request sent"""
        signout = self.selenium.find_element(By.NAME, "signout")
        signout.click()
        email = WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "email")))
        email.click()
        user = CustomUser.objects.get(pk=1)
        user.set_password("testing123") # so it can be hashed
        user.save()
        with open('api/fixtures/users.json', 'r') as file:
            email_address = json.load(file)[0]['fields']['email']
        email.send_keys(email_address)
        password = self.selenium.find_element(By.NAME, "password")
        password.click()
        password.send_keys("testing123")
        submit = self.selenium.find_element(By.NAME, "submit")
        submit.click()
        tab = WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "friend-requests-received-tab")))
        tab.click()
        accept_request = WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "accept-request"))
        )
        accept_request.click()
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.invisibility_of_element_located((By.NAME, "accept-request"))
        )