import os
import pathlib
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver import DesiredCapabilities
from selenium_recaptcha_solver import RecaptchaSolver

class Firefox_Driver():
    def __init__(self, savingpath='./'):
        # Getting the absolute path for the passed savingpath
        self.rootpath = pathlib.Path(os.getcwd())
        self.savingpath = pathlib.Path(self.rootpath, savingpath)
        self.firefox_options = Options()
        self.captcha_solver = None

    def __set_default_driver_options__(self):
        '''specifying default download directory for the particular instance of FirefoxDriver'''
        self.prefs = {'download.default_directory': self.savingpath}
        # self.firefox_options.add_argument("--no-sandbox")
        self.profile = FirefoxProfile()
        self.profile.set_preference("browser.download.dir", os.path.join(self.savingpath))
        self.profile.set_preference("browser.download.folderList", 2)
        self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        self.profile.set_preference('devtools.jsonview.enabled', False)
        self.profile.set_preference("dom.webdriver.enabled", False)
        self.profile.set_preference('useAutomationExtension', False)
        self.profile.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0")
        self.profile.update_preferences()
        self.desired = DesiredCapabilities.FIREFOX

    def __initialise_firefox_driver__(self):
        """
        Initialise firefox driver with options
        """
        self.driver = webdriver.Firefox(options=self.firefox_options)

    def modify_firefox_driver(self, *args):
        """
        Takes in variable number of arguments to modify the firefox options.
        Each arg must be a Tuple for Firefox preferences
        """
        for arg in args:
            self.profile.set_preference(*arg)

    def get_modified_firefox_driver(self, *args):
        """
        Returns modified firefox driver with default firefox options applied, if no firefox options provided as arguments.
        """
        if args:
            self.modify_firefox_driver(*args)
        else:
            self.__set_default_driver_options__()
        self.firefox_options.profile = self.profile
        self.__initialise_firefox_driver__()
        self.captcha_solver = RecaptchaSolver(driver=self.driver)
        return self.driver