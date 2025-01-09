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

class ProfileSeleniumTests(StaticLiveServerTestCase):
    port = 8000
    fixtures = ['users.json']
    
    # setting password of test user (set in fixtures) manually so it can be hashed using set_password
    user = CustomUser.objects.get(pk=1)
    user.set_password("testing123") # so it can be hashed
    user.save()

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
        # enter name
        self.selenium.get(f"{self.live_server_url}/signup")
        full_name = self.selenium.find_element(By.NAME, "name").click()
        full_name.send_keys(valid_signup_data()['name'])

        # enter email
        email = self.selenium.find_element(By.NAME, "email").click()
        email.send_keys(valid_signup_data()['email'])

        # enter password
        password_input = self.selenium.find_element(By.NAME, "password").click()
        password_input.send_keys(valid_signup_data()['password'])
        self.selenium.find_element(By.NAME, "show-password").click()

        # enter dob
        date_of_birth = self.selenium.find_element(By.NAME, "date_of_birth").click()
        date_of_birth.send_keys(valid_signup_data()['date_of_birth'].strftime('%d-%m-%Y'))

        # enter profile picture
        profile_picture = self.selenium.find_element(By.NAME, "profile_picture")
        profile_picture.send_keys(valid_signup_data()['file_path'])
        
        # submit form
        self.selenium.find_element(By.NAME, "submit").click()
        
        self.test_login()
    
    def test_login(self):
        """Testing login"""
        # sign out
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "signout"))
        ).click()

        # enter email
        email = WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "email"))
        ).click()
        email.send_keys(valid_signup_data()['email'])

        # enter password
        password = self.selenium.find_element(By.NAME, "password").click()
        password.send_keys(valid_signup_data()['password'])

        # submit form
        self.selenium.find_element(By.NAME, "submit").click()
        
        self.test_profile()


    def test_profile(self):
        """Testing editing all the user's data on their profile page"""
        self.test_profile_edit()
        self.test_add_hobby()
        self.test_send_friend_request()

    
    def test_profile_edit(self):
        """Testing editing all profile details"""
        # edit profile picture
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "remove_profile"))
        ).click()
        old_src = self.selenium.find_element(By.CSS_SELECTOR, "img.rounded-circle").get_attribute("src")
        profile_pic = self.selenium.find_element(By.NAME, "profile_pic")
        profile_pic.send_keys(valid_signup_data()['file_path2'])
        WebDriverWait(self.selenium, 10).until(
           lambda driver: driver.find_element(By.CSS_SELECTOR, "img.rounded-circle").get_attribute("src") != old_src)
        
        # edit name
        self.selenium.find_element(By.NAME, "name_edit").click()
        name = self.selenium.find_element(By.NAME, "name").click()
        name.clear()
        name.send_keys("New Name")
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "name_save"))
        ).click()
        
        # edit email
        self.selenium.find_element(By.NAME, "email_edit").click()
        email = self.selenium.find_element(By.NAME, "email").click()
        email_address = valid_signup_data()['email']+".uk"
        email.clear()
        email.send_keys(email_address)
        self.selenium.find_element(By.NAME, "email_check").click()
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "email_save"))
        ).click()
        
        # edit password
        self.selenium.find_element(By.NAME, "password_edit").click()
        current_password = self.selenium.find_element(By.NAME, "current_password").click()
        current_password.send_keys(valid_signup_data()['password'])
        new_password = self.selenium.find_element(By.NAME, "new_password").click()
        new_pass = valid_signup_data()['password']+"1"
        new_password.send_keys(new_pass)
        new_password2 = self.selenium.find_element(By.NAME, "new_password2").click()
        new_password2.send_keys(new_pass)
        self.selenium.find_element(By.NAME, "password_check").click()
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "password_save"))
        ).click()
        
        # edit dob
        self.selenium.find_element(By.NAME, "dob_edit").click()
        dob = self.selenium.find_element(By.NAME, "dob").click()
        dob.send_keys("22-03-2004")
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "dob_save"))
        ).click()
        
    def test_add_hobby(self):
        """Testing editing hobbies"""
        # navigate to hobby tab
        self.selenium.find_element(By.NAME, "hobbies").click()
        self.selenium.find_element(By.NAME, "add_hobby").click()

        # enter name
        hobby_name = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "hobby_name"))
        ).click()
        hobby_name.send_keys("Baking")
        
        # enter description
        hobby_description = self.selenium.find_element(By.NAME, "hobby_description").click()
        hobby_description.send_keys("The art of baking things.")

        # select level
        self.selenium.find_element(By.NAME, "level").click()
        self.selenium.find_element(By.NAME, "level_option").click()

        # select start date
        hobby_start_date = self.selenium.find_element(By.NAME, "hobby_start_date").click()
        hobby_start_date.send_keys("10-10-2010")

        # validate hobby details 
        self.selenium.find_element(By.NAME, "check_hobby").click()

        # save hobby
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "save_hobby"))
        ).click()

        # delete hobby
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "delete_hobby"))
        ).click()


    def test_send_friend_request(self):
        """Testing sending a friend request"""
        # navigate to users page
        self.selenium.find_element(By.LINK_TEXT, "Users").click()

        # send friend request
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "send-request"))
        ).click()
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "status")))
        
        self.test_accept_friend_request()


    def test_accept_friend_request(self):
        """Testing login as the other user and accept the freind request sent"""
        # log out
        self.selenium.find_element(By.NAME, "signout").click()
        
        # sign in as other user 
        email = WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "email"))
        ).click()
        
        # get test user email
        with open('api/fixtures/users.json', 'r') as file:
            email_address = json.load(file)[0]['fields']['email']
        email.send_keys(email_address)

        # enter test user password
        password = self.selenium.find_element(By.NAME, "password").click()
        password.send_keys("testing123")

        # submit form
        self.selenium.find_element(By.NAME, "submit").click()
        
        # navigate to friend requests receieved tab
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "friend-requests-received-tab"))
        ).click()
        
        # accept friend request
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "accept-request"))
        ).click()
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.invisibility_of_element_located((By.NAME, "accept-request"))
        )