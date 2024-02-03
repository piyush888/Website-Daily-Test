import argparse
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from drivers.chrome_driver import Chrome_Driver
from drivers.firefox_driver import Firefox_Driver
from test_flows.login_workflow import login_workflow
from test_flows.downloads_workflow import download_workflow

class WebsiteTester():
    def __init__(self, web_driver: str = "firefox"):
        if web_driver == "firefox":
            self.driver_object = self.get_webdriver(web_driver=web_driver)
            self.driver = self.driver_object.get_modified_firefox_driver()
            self.captcha_solver = self.driver_object.captcha_solver
        elif web_driver == "chrome":
            self.driver_object = self.get_webdriver(web_driver=web_driver)
            self.driver = self.driver_object.get_modified_chrome_driver()
            self.captcha_solver = self.driver_object.captcha_solver
        else:
            self.driver = self.get_webdriver(web_driver=web_driver)
        

    def get_webdriver(self, web_driver):
        if web_driver=="firefox": return Firefox_Driver()
        elif web_driver=="chrome": return Chrome_Driver()
        elif web_driver=="safari": return webdriver.Safari()
        elif web_driver=="iexplorer": return webdriver.Ie()
        elif web_driver=="webkitgtk": return webdriver.WebKitGTK()
        elif web_driver=="edge": return webdriver.Edge()
        elif web_driver=="wpewebkit": return webdriver.WPEWebKit()
        else:
            return webdriver.Chrome()


    def sel_test_website(self, website="https://aidronesoftware.com/", *args, **kwargs):
        self.driver.get(website)
        
        login_workflow(driver=self.driver, captcha_solver=self.captcha_solver, login_email=kwargs['login_email'], login_password=kwargs['login_password'], recaptcha=kwargs['recaptcha'])

        download_workflow(driver=self.driver)

        time.sleep(2)

        self.driver.close()


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("--web-driver", help = "Input your preferred web-driver", choices=['firefox', 'chrome', 'safari', 'iexplorer', 'webkitgtk', 'edge', 'wpewebkit'], default='firefox')
    parser.add_argument("--website", help = "Input your website", default='www.google.com')
    parser.add_argument("--login-email", help = "Input your login email or username")
    parser.add_argument("--login-password", help = "Input your login password")
    parser.add_argument('--recaptcha-enabled', action='store_true', help='Login is ReCAPTCHA enabled')
    
    # Read arguments from command line
    args = parser.parse_args()

    tester = WebsiteTester(web_driver=args.web_driver)
    tester.sel_test_website(website=args.website, login_email=args.login_email, login_password=args.login_password, recaptcha=args.recaptcha_enabled)