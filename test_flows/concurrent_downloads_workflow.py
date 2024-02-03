import time
import os
import pathlib
from typing import Callable
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from urllib3.exceptions import NewConnectionError, MaxRetryError
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium_recaptcha_solver import RecaptchaSolver


def check_download(download_path: str, download_filename: str, failure_event: Callable[..., None]=None):
    if is_download_complete(download_path, download_filename):
        print(f"Download of {download_filename} package has completed")
    else:
        msg = f"Download did not complete within the timeout period for {download_filename}"
        print(msg)
        if failure_event:
            failure_event(msg)


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


def download_component(driver, component_xpath: str=None):
    component = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, component_xpath)))
    component.click()
    

def download_workflow(driver, darwin_download_filename: str="drone-forge-darwin-x64-1.0.0.zip", windows_download_filename: str="drone-forge-1.0.0_Setup.exe", failure_event: Callable[..., None]=None):
    print("Navigating to Profile/Download page...")
    download_path = pathlib.Path(os.getcwd())

    # Await the loading of a Profile page button (or the downloads page button) on the webpage
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/main/nav/div/div[2]/a[1]")))
    
    element.click()

    # Download for Darwin
    print("Attempting download for Darwin Package...")
    download_component(driver=driver, component_xpath="/html/body/div/div/div/div[1]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/center/a")

    # Download for Windows
    print("Attempting download for Windows Package...")
    download_component(driver=driver, component_xpath="/html/body/div/div/div/div[1]/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/center/a")

    # Simultaneous downloads: Verify downloads concurrently
    components_parameters = [[download_path, darwin_download_filename], [download_path, windows_download_filename]]
    with ThreadPoolExecutor(max_workers=len(components_parameters)) as executor:
        futures = [executor.submit(check_download, *params) for params in components_parameters]
        for future in futures:
            future.result()


    # Perform cleanup
    for f in [darwin_download_filename, windows_download_filename]:
        del_path = os.path.join(download_path, f)
        if os.path.exists(del_path):
            os.remove(del_path)
            print(del_path, ": File deleted successfully")
        else:
            print(del_path, ": The file does not exist")