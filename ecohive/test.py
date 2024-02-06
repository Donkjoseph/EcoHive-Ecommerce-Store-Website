from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class Hosttest(TestCase):

    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000'

    def tearDown(self):
        self.driver.quit()


    def test_02_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(2)

#register from home
#         theme=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/register.html']") 
#         theme.click()
#         time.sleep(4)
#         elem = driver.find_element(By.NAME, "username")
#         elem.send_keys("seller6")
#         time.sleep(2)
#         elem = driver.find_element(By.NAME, "email")
#         elem.send_keys("nftnext12@gmail.com")
#         time.sleep(2)
#         elem = driver.find_element(By.NAME, "password1")
#         elem.send_keys("Don@2001")
#         elem = driver.find_element(By.NAME, "password2")
#         elem.send_keys("Don@2001")
#         time.sleep(4)
#         elem = driver.find_element(By.NAME, "is_seller")
#         elem.click()
#         time.sleep(4)
#         submit_button = driver.find_element(By.CSS_SELECTOR, "button#submitButton.signupbtn")
#         submit_button.click()
#         time.sleep(5)

#login from home seller
        theme=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/login.html']") 
        theme.click()
        elem = driver.find_element(By.NAME, "username")
        elem.send_keys("seller1")
        elem = driver.find_element(By.NAME, "password")
        elem.send_keys("Don@2001")
        time.sleep(2)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button#login_button.signinbtn")
        submit_button.click()
        time.sleep(5)
        browse=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/dashseller.html']")
        browse.click()
        time.sleep(5)
        browse=driver.find_element(By.CSS_SELECTOR,"a.sidebar-link[href='/addproducts']")
        browse.click()
        time.sleep(5)
        elem = driver.find_element(By.NAME, "product_name")
        elem.send_keys("rambutan")
        time.sleep(2)
        elem = driver.find_element(By.NAME, "product_description")
        elem.send_keys("good natural product")
        time.sleep(2)

        elem = driver.find_element(By.NAME, "product_price")
        elem.send_keys("250")
        time.sleep(2)

        elem = driver.find_element(By.NAME, "product_stock")
        elem.send_keys("20")
        time.sleep(2)

        select_element = Select(driver.find_element(By.NAME, "select_category"))
        select_element.select_by_value("5")
        time.sleep(2)

        file_path = r"C:\Users\donkj\Downloads\organic products\rambutan.jpg"
        elem = driver.find_element(By.NAME, "product_image")
        elem.send_keys(file_path)
        time.sleep(2)
        browse=driver.find_element(By.CSS_SELECTOR,"button#add-product-button")
        browse.click()
        time.sleep(2)
        browse=driver.find_element(By.CSS_SELECTOR,"a.btn.btn-danger[href='/viewaddproduct']")
        browse.click()
        time.sleep(2)
        browse=driver.find_element(By.CSS_SELECTOR,"a.nav-link.nav-icon-hover[data-bs-toggle='dropdown']]")
        browse.click()
        time.sleep(2)
        browse=driver.find_element(By.CSS_SELECTOR,"a.btn.btn-outline-primary.mx-3.mt-2.d-block[href='/logout/']")
        browse.click()
        time.sleep(2)
#login from home admin
#         theme=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/login.html']") 
#         theme.click()
#         elem = driver.find_element(By.NAME, "username")
#         elem.send_keys("Admin")
#         elem = driver.find_element(By.NAME, "password")
#         elem.send_keys("Don@2001")
#         time.sleep(2)
#         submit_button = driver.find_element(By.CSS_SELECTOR, "button#login_button.signinbtn")
#         submit_button.click()
#         time.sleep(5)
#         browse=driver.find_element(By.CSS_SELECTOR,"a.sidebar-link[href='/addcategory']")
#         browse.click()
#         time.sleep(5)      
#         elem = driver.find_element(By.NAME, "category_name")
#         elem.send_keys("dairyproducts")
#         time.sleep(2)
#         elem = driver.find_element(By.NAME, "category_description")
#         elem.send_keys("diry products like nuts etc")
#         time.sleep(2)
#         browse=driver.find_element(By.CSS_SELECTOR,"button.btn.btn-primary")
#         browse.click()
#         time.sleep(2)
#Add to cart 
        # theme=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/login.html']") 
        # theme.click()
        # elem = driver.find_element(By.NAME, "username")
        # elem.send_keys("customer1")
        # elem = driver.find_element(By.NAME, "password")
        # elem.send_keys("Don@2001")
        # time.sleep(2)
        # submit_button = driver.find_element(By.CSS_SELECTOR, "button#login_button.signinbtn")
        # submit_button.click()
        # time.sleep(2)
        # browse=driver.find_element(By.CSS_SELECTOR,"a#top.nav-link")
        # browse.click()
        # time.sleep(2)
        # driver.execute_script("window.scrollBy(0, 500);")
        # browse=driver.find_element(By.CSS_SELECTOR,"a.img-prod")
        # browse.click()
        # driver.execute_script("window.scrollBy(0, 500);")
        # time.sleep(2)
        # browse=driver.find_element(By.CSS_SELECTOR,"button.add-to-cart-button[name='buy_now']")
        # browse.click()
        # time.sleep(5)

if __name__ == '__main__':
    import unittest
    unittest.main()