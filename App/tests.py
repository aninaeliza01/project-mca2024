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
#         print('Clicked Login Button')

#         username_input.send_keys('amil')
#         password_input.send_keys('Amil@123')
#         login_button.click()

#         # Wait for the page to load after login
#         WebDriverWait(self.driver, 10).until(EC.url_contains('userhome'))
#         print("Successfully Redirected to Home Page")



# #|||||||||addfuel||||||########

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
#         print("Fuel Successfully Added")

    
#     def test_login_and_add_fuel(self):
#         self.login()
#         self.add_fuel()


# # ##|||||||||||place order |||||||#####
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
#         password.send_keys("Godwi@123")
#         self.driver.find_element(By.ID, "logout-link").click()
#         self.driver.implicitly_wait(5)

#         WebDriverWait(self.driver, 10).until(EC.url_contains('userhome'))

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
#         print("Successfully Placed order")

#     def tearDown(self):
#         self.driver.quit()

# if __name__ == "__main__":
#     unittest.main()

# ####||||| DELETE ORDER|||||||||||||###########
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
#         password.send_keys("Godwi@123")
#         self.driver.find_element(By.ID, "logout-link").click()
#         self.driver.implicitly_wait(5)

#         WebDriverWait(self.driver, 10).until(EC.url_contains('userhome'))


#         self.driver.get(self.base_url + '/customer_unorders')  # Update with your actual orders page URL

#         # Find the 'Place Order' button
#         place_order_button = None
#         try:
#             place_order_button = self.driver.find_element(By.CLASS_NAME, 'order-action-button.cancel')
#         except:
#             pass

#         # Click the 'Place Order' button if found
#         if place_order_button:
#             place_order_button.click()
#             print("Deleted Order Successfully")
            
#         else:
#             self.fail("Failed to find or click the 'Place Order' button")

#     def tearDown(self):
#         self.driver.quit()

# if __name__ == "__main__":
#     unittest.main()


#########search######
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UserInterfaceTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://localhost:8000"
        self.driver.implicitly_wait(10)

    def test_login_and_place_order(self):
        self.driver.get(self.base_url + '/login')
        self.assertIn("Login Form", self.driver.title)

        # Fill in login credentials and submit
        username = self.driver.find_element(By.NAME, 'username')
        password = self.driver.find_element(By.NAME, 'password')
        username.send_keys("godwin")
        password.send_keys("Godwi@123")
        self.driver.find_element(By.ID, "logout-link").click()
        self.driver.implicitly_wait(5)

        # Wait for redirection to user home page
        WebDriverWait(self.driver, 10).until(EC.url_contains('userhome'))
        search_input = self.driver.find_element(By.ID, 'locationInput')
        
        # Enter the search query
        search_input.send_keys('ne')  # Replace with your test search query
        
        # Click the search button
        search_button = self.driver.find_element(By.CSS_SELECTOR, '.search-container button')
        search_button.click()
        
        # Wait for search results to load
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'amazon-order-box')))
        
        # Assert that search results are displayed
        search_results = self.driver.find_elements(By.CLASS_NAME, 'amazon-order-box')
        self.assertGreater(len(search_results), 0)   
        time.sleep(30)
        if len(search_results) > 0:
            print("Successfully Searched results")
            
            
        else:
            print("Search results: No result.")


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
