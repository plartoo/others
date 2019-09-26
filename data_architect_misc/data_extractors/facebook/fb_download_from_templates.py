"""
Author: Phyo Thiha
Last Modified Date: September 26, 2019
Description: This script downloads the data from the report templates
(created by another script 'fb_create_templates.py') in each of the
account in FB Business Manager website.
"""


import pdb

import os
import re
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

import account_info
import fb_common


def main():
    browser = fb_common.get_chrome_browser_instance()
    fb_common.log_in(browser)
    fb_common.go_to_ads_reporting(browser, account_info.ADS_REPORTING_URL)
    report_urls = fb_common.get_urls_of_all_accounts(browser,
                                                     'https://business.facebook.com/adsmanager/reporting/manage?')

    # TODO: remove below because this is only for testing purpose
    # 'br_oc_cspr_e1 (2023550174542784)'
    report_urls = list(filter(lambda x: ('2023550174542784' in x), report_urls))

    for url in report_urls:
        print("\nFetching:", url)
        browser.get(url)
        # Wait to load all report templates or we will end up getting account names like 'Loading___'
        # time.sleep(fb_common.WAIT_TIME_IN_SEC)
        accnt_name_str = fb_common.get_account_name_and_id(browser)
        # browser.find_element_by_xpath('//span[@data-testid="manage_reports_name_cell"]').find_element_by_xpath('./following::div/button').get_attribute('innerHTML')
        downloaded_report_names = []
        report_names_xpath = '//span[@data-testid="manage_reports_name_cell"]'
        export_btn_xpath = '//button[@data-testid="export_button"]'
        for report_name_ele in browser.find_elements_by_xpath(report_names_xpath):
            report_name = report_name_ele.text.strip()
            if (not (report_name in downloaded_report_names)) and ('DoNotDelete' in report_name):
                view_report_btn = report_name_ele.find_element_by_xpath('./following::div/button')
                view_report_btn.click()
                time.sleep(fb_common.WAIT_TIME_IN_SEC) # wait for the data table in the template to load
                # fb_common.click_xpath(browser, view_report_btn_xpath)
                # 'DoNotDelete'
                fb_common.click_xpath(browser, export_btn_xpath)
                pdb.set_trace()
                print("ha")
                downloaded_report_names.append(report_name)


if __name__ == '__main__':
    main()


