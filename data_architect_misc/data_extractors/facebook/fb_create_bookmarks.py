"""
Author: Phyo Thiha
Last Modified Date: September 17, 2019
Description: This is script is used to create bookmarks on Facebook's Business Manager site.
We have >40 FB accounts and each account has about 10 report templates to create, so we
will automate creation of these bookmarks.

Note: For anyone interested, read the following resources to learn more about Selenium:
# Selenium Docs: http://selenium-python.readthedocs.io/
# http://web.archive.org/web/20190830175223/http://thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1/
# http://web.archive.org/web/20190830175349/http://thiagomarzagao.com/2013/11/14/webscraping-with-selenium-part-2/
# http://web.archive.org/web/20190830175411/http://thiagomarzagao.com/2013/11/15/webscraping-with-selenium-part-3/
# http://web.archive.org/web/20190830175437/https://www.scrapehero.com/tutorial-web-scraping-hotel-prices-using-selenium-and-python/
"""

import pdb

import os
from datetime import datetime
import re
import time

from selenium import webdriver

import account_info


# Time to wait between checking latest downloaded files in 'Download' folder
WAIT_TIME_INCREMENT_IN_SEC = 5
WAIT_TIME_LIMIT = 300

# Location of folder where Chrome driver saves the downloaded files.
# Also if you use Firefox, make sure the download behavior is set to start
# automatically (instead of prompting user to click on 'OK' button to start
# the download).
# REF: http://web.archive.org/web/20190905202224/http://kb.mozillazine.org/File_types_and_download_actions
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')
BASE_URL = 'https://business.facebook.com/login/?next=https%3A%2F%2Fbusiness.facebook.com%2F'


def log_in(browser):
    print("Logging into Business Manager.")
    browser.get(BASE_URL)
    browser.find_element_by_id('email').clear()
    browser.find_element_by_id('pass').clear()
    browser.find_element_by_id('email').send_keys(account_info.USERNAME)
    browser.find_element_by_id('pass').send_keys(account_info.PASSWORD)
    browser.find_element_by_id('loginbutton').click()


def go_to_ads_reporting(browser):
    print("Clicking on 'Ads Reporting' in hamburger menu.")
    browser.find_elements_by_xpath('//*[text()="Business Manager"]')[1].click()
    browser.find_elements_by_xpath('//*[text()="Ads Reporting"]')[0].click()


def main():
    folder_that_has_this_code = os.getcwd()
    # Note: Make sure that "chromedrive/chromedriver.exe" shares same PARENT folder as this script
    parent_folder = os.path.dirname(os.path.normpath(folder_that_has_this_code))
    chromedriver_exe_with_path = os.path.join(parent_folder , 'chromedriver', 'chromedriver.exe')
    print("\nInvoking Chrome driver at:", chromedriver_exe_with_path, "\n")
    browser = webdriver.Chrome(executable_path=chromedriver_exe_with_path)
    log_in(browser)
    go_to_ads_reporting(browser)

    # browser.close()
    pdb.set_trace()
    print("\nCreated bookmarks on FB Business Manager website.")


if __name__ == '__main__':
    main()