from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginTestCase(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  # Initialize Chrome WebDriver
        self.driver.implicitly_wait(10)   # Implicit wait for elements

    def tearDown(self):
        self.driver.quit()  # Close the browser session after each test

    def test_login(self):
        self.driver.get('http://127.0.0.1:8000/login/')

        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.ID, 'logout-link')

        username_input.send_keys('amil')
        password_input.send_keys('Amil@123')
        login_button.click()

        # Wait for the page to load after login (replace this with appropriate page load condition)
        WebDriverWait(self.driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/userhome/'))

        # Perform assertions to verify successful login
        # expected_content = 'Text or Element on Successful Login Page'
        # assert expected_content in self.driver.page_source, f"Expected content '{expected_content}' not found after login"
