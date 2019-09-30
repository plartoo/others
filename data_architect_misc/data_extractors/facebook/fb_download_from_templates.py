"""
Author: Phyo Thiha
Last Modified Date: September 26, 2019
Description: This script downloads the data from the report templates
(created by another script 'fb_create_templates.py') in each of the
account in FB Business Manager website.
"""

import pdb

from datetime import datetime
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


# Location of folder where Chrome driver saves the downloaded files.
# Also if you use Firefox, make sure the download behavior is set to start
# automatically (instead of prompting user to click on 'OK' button to start
# the download).
# REF: http://web.archive.org/web/20190905202224/http://kb.mozillazine.org/File_types_and_download_actions
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')
OUTPUT_FOLDER_NAME = 'fb_business_manager_reports'
TEMPLATE_PREFIX = 'DoNotDelete'


def download_data_export_file(browser):
    export_btn_xpath = '//button[@data-testid="export_button"]'
    export_confirm_btn_xpath = '//button[@data-testid="export-confirm-button"]'
    fb_common.click_xpath(browser, export_btn_xpath)
    fb_common.click_xpath(browser, export_confirm_btn_xpath)


def get_latest_file_in_folder(folder):
    # We will infer the latest downloaded (non-temporary) file name from getctime.
    # REF: https://stackoverflow.com/q/17958987
    # '.xlsx.crdownload' seems to be the temp download files in Windows 10 when using Chrome driver
    non_temp_files = list(filter(lambda x: not (x.endswith('.tmp') or x.endswith('.xlsx.crdownload')), os.listdir(folder)))
    return max([os.path.join(folder, f) for f in non_temp_files], key=os.path.getctime)


def wait_until_file_download_is_finished(previously_downloaded_file,
                                         download_folder,
                                         wait_time_increment, wait_time_limit):
    # IMPORTANT ASSUMPTION: here, we don't expect any parallel process to be creating
    # new files within Download folder while we are running this download process.
    # Let's busy wait until the file is downloaded (no way to detect successful page load via Selenium)
    time_waited_so_far_in_sec = 0
    while previously_downloaded_file == get_latest_file_in_folder(download_folder):
        time.sleep(wait_time_increment)
        time_waited_so_far_in_sec += wait_time_increment
        if time_waited_so_far_in_sec > wait_time_limit:  # if download is taking longer than 5 minutes, break and print error message
            print("WARNING: It seems to be taking longer than",
                  wait_time_limit,
                  ". We are skipping download for this template")
            return


def strip_date_ranges(report_template_name):
    return re.sub(r'_\d{8}_\d{8}.*','', report_template_name)


def get_output_file_name(report_template_name, report_from_date, report_to_date):
    # Decide which time frame we want to download data for (current year's YTD data by default)
    cur_date = datetime.now().strftime('%Y%m%d')
    file_name = '_'.join([strip_date_ranges(report_template_name),
                          report_from_date, report_to_date, cur_date])
    return ''.join([file_name, '.xlsx'])


def move_most_recently_downloaded_file_to_destination_folder(previously_downloaded_file,
                                                             source_folder,
                                                             destination_folder,
                                                             output_file_name):
    """Rename and move the latest downloaded file to destination folder."""
    cur_latest_file = get_latest_file_in_folder(DOWNLOAD_FOLDER)
    if (previously_downloaded_file != cur_latest_file) and (TEMPLATE_PREFIX in cur_latest_file):
        # Only proceed when the latest downloaded file is different from previously downloaded file
        new_file_path_and_name = os.path.join(destination_folder, 'test.xlsx')#output_file_name)
        print("Renaming and moving downloaded file:", get_latest_file_in_folder(source_folder),
              "\tto:", new_file_path_and_name)
        try:
            os.rename(get_latest_file_in_folder(source_folder), new_file_path_and_name)
        except FileExistsError:
            os.remove(new_file_path_and_name)
            os.rename(get_latest_file_in_folder(source_folder), new_file_path_and_name)
        except FileNotFoundError:
            pdb.set_trace()
            print('hee')
    else:
        print("WARNING: Did not find a difference between recently downloaded file "
              "and previously downloaded file:", previously_downloaded_file)
        print("Skipping the move of downloaded file...")


def main():
    browser = fb_common.get_chrome_browser_instance()
    fb_common.log_in(browser)
    reports_processed = []
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
        time.sleep(fb_common.WAIT_TIME_IN_SEC)
        accnt_name_str = fb_common.get_account_name_and_id(browser)
        downloaded_report_names = []
        report_names_xpath = '//span[@data-testid="manage_reports_name_cell"]'
        for report_name_ele in browser.find_elements_by_xpath(report_names_xpath):
            report_name = report_name_ele.text.strip()
            if (not (report_name in downloaded_report_names)) and (TEMPLATE_PREFIX in report_name):
                print("Report Name:", report_name)
                view_report_btn = report_name_ele.find_element_by_xpath('./following::div/button')
                view_report_btn.click()
                time.sleep(fb_common.WAIT_TIME_IN_SEC) # Wait for the data table in the template to load
                from_date, to_date = fb_common.get_report_date_range(browser)

                # Get the name of the latest downloaded file name in the download folder
                previously_downloaded_file = get_latest_file_in_folder(DOWNLOAD_FOLDER)
                download_data_export_file(browser)
                # Wait up to 10 mins for download
                wait_until_file_download_is_finished(previously_downloaded_file, DOWNLOAD_FOLDER,
                                                     fb_common.WAIT_TIME_IN_SEC, 600)
                destination_folder = fb_common.create_output_folder(os.getcwd(), OUTPUT_FOLDER_NAME)
                output_file_name = get_output_file_name(report_name, from_date, to_date)
                move_most_recently_downloaded_file_to_destination_folder(previously_downloaded_file,
                                                                         DOWNLOAD_FOLDER,
                                                                         destination_folder,
                                                                         output_file_name)
                downloaded_report_names.append(report_name)
            else:
                pdb.set_trace()
                print("hee")

            time.sleep(5)  # give 5 secs break before fetching another template
            print("\nData download for template:", report_name, " finished.")

    browser.close()
    print("\nFinished scraping data from RenTrak website.")


if __name__ == '__main__':
    main()
