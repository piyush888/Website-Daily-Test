import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from urllib3.exceptions import NewConnectionError, MaxRetryError
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium_recaptcha_solver import RecaptchaSolver


def login_workflow(driver, captcha_solver: RecaptchaSolver, login_email: str, login_password: str, recaptcha: bool=False):
    """
    Perform the login workflow on the login page. The driver navigates to the login page using the login button. The XPATHs must be modified for different websites.

    :params:
        - driver: Driver object.
        - captcha_solver: selenium_recaptcha_solver.RecaptchaSolver object for the driver object passed above.
        - login_email: Email/Username to be used for login.
        - login_password: Password to be used for login.
        - recaptcha: Whether the login module has a recaptcha or not.
    """
    # Await the loading of a certain element on the webpage - in this case the login button
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div/nav/div/div[2]/a[2]")))
    
    element.click()

    # Await the loading of Email and Password Field
    email_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/div/div[1]/div/form/div[1]/input")))
    email_elem.send_keys(login_email)
    password_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/div/div[1]/div/form/div[2]/input")))
    password_elem.send_keys(login_password)

    # Modify for your ReCAPTCHA element
    if recaptcha:
        print("ATTEMPTING CAPTCHA...")
        captcha_iframe = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/form/div[3]/div/div/div/div/iframe')))
        time.sleep(2)
        captcha_solver.click_recaptcha_v2(iframe=captcha_iframe)
        time.sleep(2)
    
    # Switch frame back to main window
    driver.switch_to.default_content()

    print("Trying to find Login button...")
    login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@class='w-100 btn btn-primary' and @type='submit' and contains(text(), 'Log In')]")))

    # Click on login button
    if login.is_enabled():
        login.click()
    else:
        login.click()
        login.click()