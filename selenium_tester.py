import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from urllib3.exceptions import NewConnectionError, MaxRetryError
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from drivers.chrome_driver import Chrome_Driver
from drivers.firefox_driver import Firefox_Driver

class WebsiteTester():
    def __init__(self, web_driver: str = "firefox"):
        self.driver = self.get_webdriver(web_driver=web_driver)

    def get_webdriver(self, web_driver):
        if web_driver=="firefox": return Firefox_Driver().get_modified_firefox_driver()
        elif web_driver=="chrome": return Chrome_Driver().get_modified_chrome_driver()
        elif web_driver=="safari": return webdriver.Safari()
        elif web_driver=="iexplorer": return webdriver.Ie()
        elif web_driver=="webkitgtk": return webdriver.WebKitGTK()
        elif web_driver=="edge": return webdriver.Edge()
        elif web_driver=="wpewebkit": return webdriver.WPEWebKit()
        else:
            return webdriver.Chrome()


    def sel_test_website(self, website="https://aidronesoftware.com/", *args, **kwargs):
        self.driver.get(website)
        
        self.login_workflow(login_email=kwargs['login_email'], login_password=kwargs['login_password'], recaptcha=kwargs['recaptcha'])

        self.driver.close()


    def login_workflow(self, login_email, login_password, recaptcha=False):
        # Await the loading of a certain element on the webpage - in this case the login button
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div/nav/div/div[2]/a[2]")))
        
        element.click()

        # Await the loading of Email and Password Field
        email_elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div/div/div[1]/div/form/div[1]/input")))
        email_elem.send_keys(login_email)
        password_elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div/div/div[1]/div/form/div[2]/input")))
        password_elem.send_keys(login_password)

        # Modify for your ReCAPTCHA element
        if recaptcha:
            print("ATTEMPTING CAPTCHA...")
            captcha_iframe = WebDriverWait(self.driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/form/div[3]/div/div/div/div/iframe')))
            captcha = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border")))
            time.sleep(2)
            captcha.click()
            time.sleep(2)
        
        # Switch frame back to main window
        self.driver.switch_to.default_content()

        print("Trying to find Login button...")
        login = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@class='w-100 btn btn-primary' and @type='submit' and contains(text(), 'Log In')]")))
        # login = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'btn-primary') and contains(text(), 'Log In')]")))

        # Click on login button
        if login.is_enabled():
            login.click()
        else:
            login.click()
            login.click()


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("--web-driver", help = "Input your preferred web-driver", choices=['firefox', 'chrome', 'safari', 'iexplorer', 'webkitgtk', 'edge', 'wpewebkit'], default='firefox')
    parser.add_argument("--website", help = "Input your website", default='www.google.com')
    parser.add_argument("--login-email", help = "Input your login email or username")
    parser.add_argument("--login-password", help = "Input your login password")
    parser.add_argument('--recaptcha-enabled', action='store_true', help='Login is ReCAPTCHA enabled')

    
    args = parser.parse_args()
    
    # Read arguments from command line
    args = parser.parse_args()

    tester = WebsiteTester(web_driver=args.web_driver)
    tester.sel_test_website(website=args.website, login_email=args.login_email, login_password=args.login_password, recaptcha=args.recaptcha_enabled)