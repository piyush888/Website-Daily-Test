import os
import pathlib
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class Firefox_Driver():
    def __init__(self, savingpath='./' + datetime.now().strftime("%Y%m%d")):
        # Getting the absolute path for the passed savingpath
        self.rootpath = pathlib.Path(os.getcwd())
        self.savingpath = os.path.join(self.rootpath, savingpath)
        self.firefox_options = Options()

    def __set_default_driver_options__(self):
        '''specifying default download directory for the particular instance of FirefoxDriver'''
        self.prefs = {'download.default_directory': self.savingpath}
        self.firefox_options.add_argument("--no-sandbox")
        # self.firefox_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # self.firefox_options.add_experimental_option('useAutomationExtension', False)
        # self.firefox_options.add_experimental_option('prefs', self.prefs)

    def __initialise_firefox_driver__(self):
        """
        Initialise firefox driver with options
        """
        self.driver = webdriver.Firefox(options=self.firefox_options)

    def modify_firefox_driver(self, *args):
        """
        Takes in variable number of arguments to modify the firefox options.
        """
        for arg in args:
            self.firefox_options.add_argument(arg)

    def get_modified_firefox_driver(self, *args):
        """
        Returns modified firefox driver with default firefox options applied, if no firefox options provided as arguments.
        """
        if args:
            self.modify_firefox_driver(*args)
        else:
            self.__set_default_driver_options__()
        self.__initialise_firefox_driver__()
        return self.driver