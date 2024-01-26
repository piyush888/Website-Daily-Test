import os
import pathlib
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Chrome_Driver():
    def __init__(self, savingpath='./' + datetime.now().strftime("%Y%m%d")):
        # Getting the absolute path for the passed savingpath
        self.rootpath = pathlib.Path(os.getcwd())
        self.savingpath = os.path.join(self.rootpath, savingpath)
        self.chrome_options = Options()

    def __set_default_driver_options__(self):
        '''specifying default download directory for the particular instance of ChromeDriver'''
        self.prefs = {'download.default_directory': self.savingpath}
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_experimental_option('prefs', self.prefs)

    def __initialise_chrome_driver__(self):
        """
        Initialise chrome driver with options
        """
        self.driver = webdriver.Chrome(options=self.chrome_options)

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
        return self.driver