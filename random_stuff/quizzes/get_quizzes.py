import pdb

import os
from datetime import datetime
import re
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import account_info


# Time to wait between checking latest downloaded files in 'Download' folder
WAIT_TIME_INCREMENT_IN_SEC = 5
WAIT_TIME_LIMIT = 300
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')

BASE_URL = 'https://leetcode.com/accounts/login/'
ALL_PROBLEMS_URL = 'https://leetcode.com/problemset/all/'

def log_in(browser):
    print("Logging in...")
    browser.get(BASE_URL)
    username_field = '//input[@name="login"]'
    pwd_field = '//input[@name="password"]'
    sign_in_button = '//span[contains(text(),"Sign In")]'

    username_ele = WebDriverWait(browser, 10).until(ec.visibility_of_element_located((By.XPATH, username_field)))
    username_ele.clear()
    username_ele.send_keys(account_info.USERNAME)
    pwd_ele = WebDriverWait(browser, 10).until(ec.visibility_of_element_located((By.XPATH, pwd_field)))
    pwd_ele.clear()
    pwd_ele.send_keys(account_info.PWD)

    # element_to_be_clickable is not useful, so we had to sleep 5 seconds
    print("Waiting for 5 secs until the sign in button shows up")
    time.sleep(5)
    sign_in_ele = WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, sign_in_button)))
    sign_in_ele.click()

# def fetch_all_problems_page(browser):


def main():
    folder_that_has_this_code = os.getcwd()
    # Note: Make sure that "chromedrive/chromedriver.exe" shares same PARENT folder as this script
    parent_folder = os.path.dirname(os.path.normpath(folder_that_has_this_code))
    chromedriver_exe_with_path = os.path.join(parent_folder, 'chromedriver', 'chromedriver.exe')

    print("\nInvoking Chrome driver at:", chromedriver_exe_with_path, "\n")
    browser = webdriver.Chrome(executable_path=chromedriver_exe_with_path)
    browser.get(BASE_URL)
    log_in(browser)

    browser.get('https://leetcode.com/problems/immediate-food-delivery-i/')
    qce = browser.find_element_by_xpath('//*[contains(@class,"content")]')
    # https://stackoverflow.com/questions/32391303/how-to-scroll-to-the-end-of-the-page-using-selenium-in-python
    # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
    # https://stackoverflow.com/questions/31248804/is-it-possible-to-locate-element-by-partial-id-match-in-selenium

    pdb.set_trace()
    print('haha')
    # browser.close()


if __name__ == '__main__':
    main()
