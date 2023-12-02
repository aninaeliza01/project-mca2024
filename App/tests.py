# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class LoginTestCase(TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()  # Initialize Chrome WebDriver
#         self.driver.implicitly_wait(10)   # Implicit wait for elements

#     def tearDown(self):
#         self.driver.quit()  # Close the browser session after each test

#     def test_login(self):
#         self.driver.get('http://127.0.0.1:8000/login/')

#         username_input = self.driver.find_element(By.NAME, 'username')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.ID, 'logout-link')

#         username_input.send_keys('amil')
#         password_input.send_keys('Amil@123')
#         login_button.click()

#         # Wait for the page to load after login (replace this with appropriate page load condition)
#         WebDriverWait(self.driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/userhome/'))

#         # Perform assertions to verify successful login
#         # expected_content = 'Text or Element on Successful Login Page'
#         # assert expected_content in self.driver.page_source, f"Expected content '{expected_content}' not found after login"

##|||||||||addfuel||||||########

# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time  # Add the time library

# class WebAppTests(TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)

#     def tearDown(self):
#         self.driver.quit()

#     def login(self):
#         self.driver.get('http://127.0.0.1:8000/login/')
#         username_input = self.driver.find_element(By.NAME, 'username')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.ID, 'logout-link')
#         username_input.send_keys('gayathri')  # Replace with your actual username
#         password_input.send_keys('Gayathri@123')  # Replace with your actual password
#         login_button.click()
#         WebDriverWait(self.driver, 10).until(EC.url_to_be('http://127.0.0.1:8000/pumphome/'))

#     def add_fuel(self):
#         self.driver.get('http://127.0.0.1:8000/fuel/')
#         fuel_type = self.driver.find_element(By.NAME, 'fueltype')
#         fuel_type.send_keys('Diesel')
#         price = self.driver.find_element(By.NAME, 'price')
#         price.send_keys('50')
#         add_fuel_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Add Fuel')]")
#         add_fuel_button.click()
#         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table//tr/td[contains(text(),'Diesel')]")))

    
#     def test_login_and_add_fuel(self):
#         self.login()
#         self.add_fuel()


# ##|||||||||||place order |||||||#####
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support import expected_conditions as EC

# class UserInterfaceTests(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.base_url = "http://localhost:8000"
#         self.driver.implicitly_wait(50)

#     def test_login_and_place_order(self):
#         self.driver.get(self.base_url + '/login')
#         self.assertIn("Login Form", self.driver.title)

#         username = self.driver.find_element(By.NAME, 'username')
#         password = self.driver.find_element(By.NAME, 'password')
#         username.send_keys("godwin")
#         password.send_keys("Godwin@123")
#         self.driver.find_element(By.ID, "logout-link").click()
#         self.driver.implicitly_wait(5)

#         self.assertIn("userhome", self.driver.current_url)

#         # Scroll to the 'Place Order' button
#         place_order_button = self.driver.find_element(By.ID, "placeorder")
#         self.driver.execute_script("arguments[0].scrollIntoView();", place_order_button)
        
#         # Wait for the 'Place Order' button to be clickable
#         place_order_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "placeorder")))
#         place_order_button.click()

#         # Assert if the user is redirected to the place order page
#         self.assertIn("place_order", self.driver.current_url)

#         # Now, interact with the form elements to place an order
#         fuel_type_dropdown = Select(self.driver.find_element(By.ID, 'fuel_type'))
#         fuel_type_dropdown.select_by_visible_text('petrol')  # Replace 'Your Fuel Type' with the actual option text

#         # Select Quantity
#         quantity_dropdown = Select(self.driver.find_element(By.ID, 'quantity'))
#         quantity_dropdown.select_by_value('1')  # Replace '1' with the desired quantity value

#         # Enter Delivery Point
#         delivery_point_input = self.driver.find_element(By.ID, 'delivery_point')
#         delivery_point_input.send_keys('123 Example St, City')  # Replace with the actual delivery point

#         # Select Payment Method
#         payment_method_dropdown = Select(self.driver.find_element(By.ID, 'payment_method'))
#         payment_method_dropdown.select_by_visible_text('Credit Card')  # Replace with the desired payment method

#         # Click on the 'Place Order' button
#         place_order_button = self.driver.find_element(By.ID, 'submit-button')
#         self.driver.execute_script("arguments[0].scrollIntoView();", place_order_button)
#         place_order_button.click()

#         # Assert if the order was placed successfully or if the user was redirected to a success page
#         self.assertIn("ordersummary", self.driver.current_url)  # Update with your success URL

#     def tearDown(self):
#         self.driver.quit()

# if __name__ == "__main__":
#     unittest.main()

#####||||| DELETE ORDER|||||||||||||###########

# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By

# class PlaceOrderAfterLoginTest(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.base_url = "http://localhost:8000"  # Replace this with your base URL
#         self.driver.maximize_window()
#         self.driver.implicitly_wait(10)

#     def test_login_and_place_order(self):
#         self.driver.get(self.base_url + '/login')
#         self.assertIn("Login Form", self.driver.title)

#         username = self.driver.find_element(By.NAME, 'username')
#         password = self.driver.find_element(By.NAME, 'password')
#         username.send_keys("godwin")
#         password.send_keys("Godwin@123")
#         self.driver.find_element(By.ID, "logout-link").click()
#         self.driver.implicitly_wait(5)
       
#         self.driver.get(self.base_url + '/customer_unorders')  # Update with your actual orders page URL

#         # Find and click the 'Place Order' button
#         place_order_button = self.driver.find_element(By.CLASS_NAME, 'order-action-form')
#         place_order_button.click()

        
#         self.assertIn("customer_orders", self.driver.current_url)

#     def tearDown(self):
#         self.driver.quit()

# if __name__ == "__main__":
#     unittest.main()
