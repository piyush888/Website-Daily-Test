import os
import pathlib
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_recaptcha_solver import RecaptchaSolver

class Chrome_Driver():
    def __init__(self, savingpath='./'):
        # Getting the absolute path for the passed savingpath
        self.rootpath = pathlib.Path(os.getcwd())
        self.savingpath = os.path.join(pathlib.Path(self.rootpath, savingpath))
        self.chrome_options = Options()
        self.captcha_solver = None
        self.service = Service(ChromeDriverManager().install())

    def __set_default_driver_options__(self):
        '''specifying default download directory for the particular instance of ChromeDriver'''
        self.prefs = {'download.default_directory': self.savingpath}
        self.chrome_options.add_argument("--no-sandbox")
        # self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_experimental_option('prefs', self.prefs)

    def __initialise_chrome_driver__(self):
        """
        Initialise chrome driver with options
        """
        self.driver = webdriver.Chrome(options=self.chrome_options, service=self.service)

    def modify_chrome_driver(self, *args):
        """
        Takes in variable number of arguments to modify the chrome options.
        """
        for arg in args:
            self.chrome_options.add_argument(arg)

    def get_modified_chrome_driver(self, *args):
        """
        Returns modified chrome driver with default chrome options applied, if no chrome options provided as arguments.
        """
        if args:
            self.modify_chrome_driver(*args)
        else:
            self.__set_default_driver_options__()
        self.__initialise_chrome_driver__()
        self.captcha_solver = RecaptchaSolver(driver=self.driver)
        return self.driver