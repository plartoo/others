"""
Author: Phyo Thiha
Last Modified Date: October 1, 2019
Description: This script downloads the data from the report templates
(created by another script 'fb_create_templates.py') in each of the
account in FB Business Manager website.
"""

import pdb

from datetime import datetime
import os
import re
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import fb_common


# Location of folder where Chrome driver saves the downloaded files.
# Also if you use Firefox, make sure the download behavior is set to start
# automatically (instead of prompting user to click on 'OK' button to start
# the download).
# REF: http://web.archive.org/web/20190905202224/http://kb.mozillazine.org/File_types_and_download_actions
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')
OUTPUT_FOLDER_NAME = 'fb_business_manager_reports'
TEMPLATE_PREFIX = 'DoNotDelete'
# How long we should wait while the file is being downloaded
WAIT_TIME_INCREMENT_IN_SEC = 5
WAIT_TIME_LIMIT_IN_SEC = 600


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
        new_file_path_and_name = os.path.join(destination_folder, output_file_name)#'test.xlsx')
        print("Renaming and moving downloaded file:", get_latest_file_in_folder(source_folder),
              "\tto:", new_file_path_and_name)
        try:
            os.rename(get_latest_file_in_folder(source_folder), new_file_path_and_name)
        except FileExistsError:
            os.remove(new_file_path_and_name)
            os.rename(get_latest_file_in_folder(source_folder), new_file_path_and_name)
        except FileNotFoundError:
            # NOTE: this could be because Windows has 260-character limit on paths
            # https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file#maximum-path-length-limitation
            # It doesn't seem to be an issue when using Python 3.6+ on Windows 10 machine
            print("ERROR: error in moving the file. Check the code to see developer's note.")
    else:
        print("WARNING: Did not find a difference between recently downloaded file "
              "and previously downloaded file:", previously_downloaded_file)
        print("Skipping the move of downloaded file...")


def get_all_report_names_in_current_dom(browser):
    report_name_xpath = '//div[@class="ReactVirtualized__Grid__innerScrollContainer"]//a[@href="#"]/div'
    WebDriverWait(browser, fb_common.WAIT_TIME_IN_SEC)\
        .until(ec.presence_of_element_located((By.XPATH, report_name_xpath)))
    return [r.text for r in browser.find_elements_by_xpath(report_name_xpath)]


def fetch_list_of_all_relevant_reports(browser):
    all_reports = []
    scroll_div = '//div[@class="ReactVirtualized__Grid__innerScrollContainer"]/parent::div'
    cur_scroll_pos = 0;
    scroll_length = 300;

    reports_in_dom = get_all_report_names_in_current_dom(browser)
    # i = 0
    while not set(reports_in_dom).issubset(set(all_reports)):
        for r in reports_in_dom:
            if not r in all_reports: #and (TEMPLATE_PREFIX in r):
                # I won't use 'set' because I want to maintain the ordering
                # print(str(i), ":", r)
                all_reports.append(r)
                # i += 1

        cur_scroll_pos += scroll_length
        js = ''.join(['arguments[0].scrollTop=', str(cur_scroll_pos), ';'])
        # Scroll 600 pixel down and repeat
        browser.execute_script(js, browser.find_elements_by_xpath(scroll_div)[-1])
        reports_in_dom = get_all_report_names_in_current_dom(browser)
    return all_reports


def scroll_to_report_name(browser, report_name):
    cur_scroll_pos = 0;
    scroll_length = 300;
    reports_in_dom = get_all_report_names_in_current_dom(browser)
    scroll_div = '//div[@class="ReactVirtualized__Grid__innerScrollContainer"]/parent::div'
    while not report_name in reports_in_dom:
        cur_scroll_pos += scroll_length
        js = ''.join(['arguments[0].scrollTop=', str(cur_scroll_pos), ';'])
        # Scroll 600 pixel down and repeat
        browser.execute_script(js, browser.find_elements_by_xpath(scroll_div)[-1])
        reports_in_dom = get_all_report_names_in_current_dom(browser)


def main():
    destination_folder = fb_common.create_output_folder(os.getcwd(), OUTPUT_FOLDER_NAME)
    browser = fb_common.get_chrome_browser_instance()
    fb_common.log_in(browser)
    fb_common.go_to_ads_reporting(browser)

    print("Fetching list of all available report template names...")
    all_reports = fetch_list_of_all_relevant_reports(browser)
    print("Num of all unfiltered reports:", len(all_reports))
    all_filtered_reports = all_reports
    # all_filtered_reports = list(filter(lambda x: (TEMPLATE_PREFIX in x), all_reports))
    print("Num of filtered reports:", len(all_filtered_reports))

    downloaded_report_names = []
    i = 0
    for report_name in [r for r in all_filtered_reports if '0_Test_CO_OC_UltraSoft_e1' in r]:#all_filtered_reports:
        if not (report_name in downloaded_report_names):
            i += 1
            print("\n", str(i), ".Trying to download report:", report_name)
            fb_common.go_to_ads_reporting(browser)
            time.sleep(fb_common.WAIT_TIME_IN_SEC)
            scroll_to_report_name(browser, report_name)
            time.sleep(fb_common.WAIT_TIME_IN_SEC)
            report_xpath = '//div[contains(text(),"{0}")]//parent::a//parent::span//parent::div//parent::div//parent::div'.format(report_name)
            # TODO: maybe instead of  using click_xpath, try this JS click approach because we often get ElementClickInterceptedException here
            # https://stackoverflow.com/a/48667924/1330974
            fb_common.click_xpath(browser, report_xpath)
            from_date, to_date = fb_common.get_report_date_range(browser)

            # Get the name of the latest downloaded file name in the download folder
            previously_downloaded_file = get_latest_file_in_folder(DOWNLOAD_FOLDER)
            download_data_export_file(browser)
            # Wait up to 10 mins for download
            wait_until_file_download_is_finished(previously_downloaded_file, DOWNLOAD_FOLDER,
                                                 WAIT_TIME_INCREMENT_IN_SEC,
                                                 WAIT_TIME_LIMIT_IN_SEC)
            output_file_name = get_output_file_name(report_name, from_date, to_date)
            move_most_recently_downloaded_file_to_destination_folder(previously_downloaded_file,
                                                                     DOWNLOAD_FOLDER,
                                                                     destination_folder,
                                                                     output_file_name)
            downloaded_report_names.append(report_name)
            print("\nData download for template:", report_name, " finished.")

    browser.close()
    print("\nFinished scraping data from FB Business Manager website.")


if __name__ == '__main__':
    main()
