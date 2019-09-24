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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

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
    print("\nClicking on 'Ads Reporting' in hamburger menu.")
    browser.find_elements_by_xpath('//*[text()="Business Manager"]')[1].click()
    browser.find_elements_by_xpath('//*[text()="Ads Reporting"]')[0].click()


def main():
    folder_that_has_this_code = os.getcwd()
    # Note: Make sure that "chromedrive/chromedriver.exe" shares same PARENT folder as this script
    parent_folder = os.path.dirname(os.path.normpath(folder_that_has_this_code))
    chromedriver_exe_with_path = os.path.join(parent_folder , 'chromedriver', 'chromedriver.exe')
    print("\nInvoking Chrome driver at:", chromedriver_exe_with_path, "\n")
    browser = webdriver.Chrome(executable_path=chromedriver_exe_with_path)
    # browser.implicitly_wait(5)
    log_in(browser)
    go_to_ads_reporting(browser)

    accounts_dropdown = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC)\
        .until(ec.element_to_be_clickable((By.XPATH, '//div[@role="toolbar"]/*/button'))) # '//div[@role="toolbar"]/*/button[1]/div/span/i'
    # accounts_dropdown = browser.find_element_by_xpath('//div[@role="toolbar"]/*/button[1]/div/span')
    accounts_dropdown.click()

    accounts = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC)\
        .until(ec.presence_of_element_located((By.XPATH, '//a[@data-testid="big-ad-account-selector-item"]//*//div[contains(text(),"Account #")]')))
    # account_names_ids = [e.text for e in browser.find_elements_by_xpath('//a[@data-testid="big-ad-account-selector-item"]//*//div[contains(text(),"Account #")]')]
    # We need to fetch URLs like this: https://business.facebook.com/adsmanager/reporting/view?act=287663358591653&business_id=1863182507246219
    report_urls = [''.join(['https://business.facebook.com/adsmanager/reporting/view?',
                              re.search('.*(act.*)', e.get_attribute('href'), re.I)[1]])
                   for e in browser.find_elements_by_xpath('//a[@data-testid="big-ad-account-selector-item"]')]

    breakdowns_and_metrics_xpaths = {
        'Campaign Name': '//span[text()="Campaign Name"]',
        'Ad Set Name': '//span[text()="Ad Set Name"]',
        'Ad Name': '//span[text()="Ad Name"]',
        'Campaign ID': '//span[text()="Campaign ID"]',
        'Ad Set ID': '//span[text()="Ad Set ID"]',
        'Ad ID': '//span[text()="Ad ID"]',

        'Day': '//span[text()="Day"]',

        'Age': '//span[text()="Age"]',
        'Gender': '//span[text()="Age"]',
        'Country': '//span[text()="Country"]',
        'Impression Device': '//span[text()="Impression Device"]',
        'Platform': '//span[text()="Platform"]',
        'Placement': '//span[text()="Placement"]',
        'Device Platform': '//span[text()="Device Platform"]',
        'Product ID': '//span[text()="Product ID"]',

        'Destination': '//span[text()="Destination"]',
        'Video View Type': '//span[text()="Video View Type"]',
        'Video Sound': '//span[text()="Video Sound"]',
        'Carousel Card': '//span[text()="Carousel Card"]',

        'Objective': '//span[text()="Objective"]',
    }

    level_options = ['Campaign Name', 'Ad Set Name', 'Ad Name', 'Campaign ID', 'Ad Set ID', 'Ad ID']
    time_options = ['Day']
    delivery_options = ['Age', 'Gender', 'Country', 'Impression Device', 'Platform', 'Placement', 'Device Platform', 'Product ID']
    action_options = ['Destination', 'Video View Type', 'Video Sound', 'Carousel Card']
    breakdowns_settings_options = ['Objective']
    performance_options = ['Results', 'Reach', 'Frequency', 'Impressions', 'Delivery', 'Amount Spent',
                                   'Clicks (All)', 'Cost per Result', 'Cost per 1,000 People Reached',
                                   'CPM (Cost per 1,000 Impressions)', 'Ad Delivery', 'Ad Set Delivery',
                                   'Campaign Delivery']
    engagement_options = ['Unique 2-Second Continuous Video Views', '2-Second Continuous Video Views']


    # metrics
    # 'div[@role="tablist"]/li[2]'
    for url in report_urls:
        print("\nFetching:", url)
        browser.get(url)
        accnt_name_id = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC)\
            .until(ec.presence_of_element_located((By.XPATH, '//div[@role="toolbar"]/*/button/*/div[@data-hover="tooltip"]')))
        # accnt_name_id = browser.find_element_by_xpath('//div[@role="toolbar"]/*/button/*/div[@data-hover="tooltip"]').text
        print("\nCreating report templates for accnt:", accnt_name_id.text)
        try:
            # create_btn = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC)\
            #     .until(ec.presence_of_element_located((By.XPATH, '//div[text()="Create"]')))
            create_btn = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC)\
                .until(ec.element_to_be_clickable((By.XPATH, '//div[text()="Create"]')))
            # create_btn = browser.find_element_by_xpath('//div[text()="Create"]')
            create_btn.click()
        except TimeoutException:
            # this means, we are redirected to 'All Reports' page because this account didn't have any prior report templates created
            print("No report template exists, so we are now in the 'All Reports' page and we'll be creating new report templates.")


        # click on metrics tab
        # browser.find_elements_by_xpath('//span[text()="Metrics"]/parent::div')[0].click()
        pdb.set_trace()
        print("aha")

    # browser.close()
    pdb.set_trace()
    print("\nCreated bookmarks on FB Business Manager website.")


if __name__ == '__main__':
    main()