import datetime, os, time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 
from api.models import CustomUser

# https://docs.djangoproject.com/en/5.1/intro/tutorial05/

def valid_signup_data() -> dict:
    """Returns a dict of valid data for a Signup Form"""
    # git_root_dir = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(git_root_dir, "test.png")
    # file_path2 = os.path.join(git_root_dir, "test2.png")
    return {
        'username': 'test_email@test.com',
        'name': 'test name',
        'email': 'testemail@test.com',
        'password': 'test_password',
        'date_of_birth': datetime.date.today(),
        # 'file_path': file_path,
        # 'file_path2': file_path2
    }

class ProfileSeleniumTests(StaticLiveServerTestCase):
    port = 8000
    fixtures = ['hobbies.json', 'users.json']
    

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        
 
    @classmethod 
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    
    def test_app(self):
        self.signup()
        self.login()
        self.profile()
        self.age_filter()
        self.send_friend_request()
        self.accept_friend_request()


    def signup(self):
        """Testing account creation / signup"""
        # enter name
        self.selenium.get(f"{self.live_server_url}/signup/")
        full_name = self.selenium.find_element(By.NAME, "name")
        full_name.click()
        full_name.send_keys(valid_signup_data()['name'])

        # enter email
        email = self.selenium.find_element(By.NAME, "email")
        email.click()
        email.send_keys(valid_signup_data()['email'])

        # enter password
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.click()
        password_input.send_keys(valid_signup_data()['password'])
        self.selenium.find_element(By.NAME, "show-password").click()

        # enter dob
        date_of_birth = self.selenium.find_element(By.NAME, "date_of_birth")
        date_of_birth.click()
        date_of_birth.clear()
        date_of_birth.send_keys(valid_signup_data()['date_of_birth'].strftime('%d-%m-%Y'))

        # enter profile picture
        # profile_picture = self.selenium.find_element(By.NAME, "profile_picture")
        # profile_picture.send_keys(valid_signup_data()['file_path'])
        
        # submit form
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.visibility_of_element_located((By.NAME, "submit"))
        ).click()
        

    def login(self):
        """Testing login"""
        # sign out
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "signout"))
        ).click()

        # enter email
        try:
            email = self.selenium.find_element(By.NAME, "email")
            email.click()
            email.send_keys(valid_signup_data()['email'])
        except:
            email = self.selenium.find_element(By.NAME, "email")
            email.click()
            email.send_keys(valid_signup_data()['email'])

        # enter password
        password = self.selenium.find_element(By.NAME, "password")
        password.click()
        password.send_keys(valid_signup_data()['password'])

        # submit form
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "submit"))
        ).click()
        

    def profile(self):
        """Testing editing all the user's data on their profile page"""
        self.profile_edit()
        self.add_hobby()

    
    def profile_edit(self):
        """Testing editing all profile details"""
        # edit profile picture
        # WebDriverWait(self.selenium, 10).until(
        #     expected_conditions.element_to_be_clickable((By.NAME, "remove_profile"))
        # ).click() 

        # profile_pic = self.selenium.find_element(By.NAME, "profile_pic")
        # profile_pic.send_keys(valid_signup_data()['file_path2'])

        # edit name
        self.selenium.find_element(By.NAME, "name_edit").click()
        name = self.selenium.find_element(By.NAME, "name")
        name.click()
        name.clear()
        name.send_keys("New Name")
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "name_save"))
        ).click()
        
        # edit email
        self.selenium.find_element(By.NAME, "email_edit").click()
        email = self.selenium.find_element(By.NAME, "email")
        email.click()
        email.clear()
        email.clear()
        email.send_keys("testing123@gmail.com")
        self.selenium.find_element(By.NAME, "email_check").click()
        try:
            WebDriverWait(self.selenium, 10).until(
                expected_conditions.element_to_be_clickable((By.NAME, "email_save"))
            ).click()
        except:
            WebDriverWait(self.selenium, 10).until(
                expected_conditions.element_to_be_clickable((By.NAME, "email_save"))
            ).click()
        
        # edit password
        self.selenium.find_element(By.NAME, "password_edit").click()
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
        self.selenium.find_element(By.NAME, "password_check").click()
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "password_save"))
        ).click()
        
        # edit dob
        dob_button = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "dob_edit"))
        )
        self.selenium.execute_script("arguments[0].scrollIntoView();", dob_button)
        dob_button.click()
        dob = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "dob"))
        )
        dob.click()
        dob.send_keys("22-03-2004")
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "dob_save"))
        ).click()
        
    def add_hobby(self):
        """Testing editing hobbies"""
        # navigate to hobby tab
        self.selenium.find_element(By.NAME, "hobbies").click()
        self.selenium.find_element(By.NAME, "add_hobby").click()

        # add new hobby button click
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "add-hobby"))
        ).click()

        # enter name
        hobby_name = WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "hobby_name"))
        )
        hobby_name.click()
        hobby_name.send_keys("Baking")
        
        # enter description
        hobby_description = self.selenium.find_element(By.NAME, "hobby_description")
        hobby_description.click()
        hobby_description.send_keys("The art of baking things.")

        # select level
        self.selenium.find_element(By.NAME, "level").click()
        self.selenium.find_element(By.NAME, "level_option").click()

        # select start date
        hobby_start_date = self.selenium.find_element(By.NAME, "hobby_start_date")
        hobby_start_date.click()
        hobby_start_date.send_keys("10-10-2010")

        # validate hobby details 
        self.selenium.find_element(By.NAME, "check_hobby").click()

        # save hobby
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.NAME, "save_hobby"))
        ).click()

        # delete hobby
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.visibility_of_element_located((By.NAME, "delete_hobby"))
        ).click()

    
    def age_filter(self):
        """Test the users page with age filtering"""

        # navigate to user page 
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Users"))
        ).click()

        # wait for the filtering input to appear and interact with it
        WebDriverWait(self.selenium, 15).until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Min Age']"))
        )
        WebDriverWait(self.selenium, 15).until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Max Age']"))
        )
        
        # Set the Min and Max age filters
        min_age_input = self.selenium.find_element(By.CSS_SELECTOR, "input[placeholder='Min Age']")
        max_age_input = self.selenium.find_element(By.CSS_SELECTOR, "input[placeholder='Max Age']")

        # Clear any pre-filled values and set new values
        min_age_input.clear()
        min_age_input.send_keys("18")

        max_age_input.clear()
        max_age_input.send_keys("30")

        # submit filter
        apply_filter_button = self.selenium.find_element(By.NAME, "apply_filter")
        apply_filter_button.click()

        WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "user-list"))
        )


    def send_friend_request(self):
        """Testing sending a friend request"""
        # send friend request
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.visibility_of_element_located((By.NAME, "send-request"))
        ).click()
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.visibility_of_element_located((By.NAME, "status")))
        

    def accept_friend_request(self):
        """Testing login as the other user and accept the freind request sent"""
        # log out
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.visibility_of_element_located((By.NAME, "signout"))
        ).click()
        
        # setting password of test user (set in fixtures) manually so it can be hashed using set_password
        user = CustomUser.objects.get(pk=3)
        user.set_password("testing123") # so it can be hashed
        user.save()

        # sign in as other user 
        email = WebDriverWait(self.selenium, 10).until(
            expected_conditions.visibility_of_element_located((By.NAME, "email"))
        )
        email.click()
        email_address = "bobb@gmail.com"
        email.send_keys(email_address)
        password = self.selenium.find_element(By.NAME, "password")
        password.click()
        password.send_keys("testing123")

        # submit form
        self.selenium.find_element(By.NAME, "submit").click()
        
        # navigate to friend requests receieved tab
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.visibility_of_element_located((By.ID, "friend-requests-received-tab"))
        ).click()

        # accept friend request
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.visibility_of_element_located((By.NAME, "accept-request"))
        ).click()
        time.sleep(3)