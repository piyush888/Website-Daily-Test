import time
import os
import pathlib
from typing import Callable
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from urllib3.exceptions import NewConnectionError, MaxRetryError
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium_recaptcha_solver import RecaptchaSolver


def is_download_complete(download_path, file_name):
    print("Polling for download finish for 5 minutes...")
    timeout = 300  # Maximum time to wait for the download in seconds
    time_elapsed = 0
    while time_elapsed < timeout:
        # condition for monitoring firefox downloads
        if any(".part" in f for f in os.listdir(download_path)):
            time.sleep(1)
            time_elapsed += 1
            continue
        if any(file_name == f for f in os.listdir(download_path)):
            return True
        time.sleep(1)
        time_elapsed += 1
    return False


def download_workflow(driver, darwin_download_filename: str="drone-forge-darwin-x64-1.0.0.zip", windows_download_filename: str="drone-forge-1.0.0_Setup.exe", failure_event: Callable[..., None]=None):
    print("Navigating to Profile/Download page...")
    download_path = pathlib.Path(os.getcwd())

    # Await the loading of a Profile page button (or the downloads page button) on the webpage
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/main/nav/div/div[2]/a[1]")))
    
    element.click()

    # Download for Darwin
    print("Attempting download for Darwin Package...")
    download_darwin = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/center/a")))
    download_darwin.click()
    if is_download_complete(download_path, darwin_download_filename):
        print("Download of Darwin package has completed")
    else:
        msg = "Download did not complete within the timeout period for darwin"
        print(msg)
        if failure_event:
            failure_event(msg)

    # Download for Windows
    print("Attempting download for Windows Package...")
    download_windows = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/center/a")))
    download_windows.click()
    if is_download_complete(download_path, windows_download_filename):
        print("Download of Windows package has completed")
    else:
        msg = "Download did not complete within the timeout period for windows"
        print(msg)
        if failure_event:
            failure_event(msg)

    # Perform cleanup
    for f in [darwin_download_filename, windows_download_filename]:
        del_path = os.path.join(download_path, f)
        if os.path.exists(del_path):
            os.remove(del_path)
            print(del_path, ": File deleted successfully")
        else:
            print(del_path, ": The file does not exist")