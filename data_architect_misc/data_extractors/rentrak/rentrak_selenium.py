import pdb

"""
Author: Phyo Thiha
Last Modified Date: August 30, 2019
Description: This is a Selenium script used to download data from RenTrak's website. 
For anyone interested, read the following resources to learn more about Selenium:
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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import account_info


def replace_nth_str(orig_str, to_replace_str, with_new_str, n):
    # Replace n-th occurrence of string (to_replace_str) with new string
    # (with_new_str) in the original string (orig_str)
    # Slightly modified version of: https://stackoverflow.com/a/35091558/1330974
    where = [m.start() for m in re.finditer(to_replace_str, orig_str)]
    if not where:
        # if no match found, just return the original string
        return orig_str

    where = where[n-1]
    before = orig_str[:where]
    after = orig_str[where:]
    after = after.replace(to_replace_str, with_new_str, 1)
    return ''.join([before, after])


def get_latest_file_in_folder(folder):
    # We will infer latest downloaded (non-temporary) file name from getctime.
    # REF: https://stackoverflow.com/q/17958987
    non_temp_files = list(filter(lambda x: not x.endswith('.tmp'), os.listdir(folder)))
    return max([os.path.join(folder, f) for f in non_temp_files], key=os.path.getctime)


def correct_ampersand_character(str_with_ampersand):
    # Replace '&amp;' in HTML decode string to '&' (correction)
    return re.sub(r'&amp;', '&', str_with_ampersand)


def sanitize_name(name):
    # Replace characters "/ \ ? < > " * | :" that are not valid for file names in Windows (and '/' for Mac and Unix)
    # Finally replaces double space characters to single space character for aesthetic reason
    # Example networks that need this:
    # ['A&amp;E', 'Azteca (Broadcast)', 'Azteca (Cable)', 'BET: Black Entertainment Television',
    # 'Cartoon Network/Adult Swim', 'De Película', 'E! - Entertainment Television', "God's Learning Channel",
    # 'Hallmark Movies &amp; Mysteries', 'History Channel en Español', 'Nickelodeon/Nick-at-Nite',
    # 'TV Land/TV Land Classic', 'Utilisima - TV / Canal', 'V-me TV (Cable)']
    return re.sub(r'\s+', ' ', re.sub(r'[\\\/\?<>\"\*|:]', ' ', correct_ampersand_character(name)))


WAIT_TIME_INCREMENT_IN_SEC = 5
WAIT_TIME_LIMIT = 300

# Define the location of folder where Chrome driver saves downloaded files
# Also if you use Firefox, make sure the download behavior is set to start
# automatically (instead of user having to click on 'OK' button to start
# the download).
# REF: http://web.archive.org/web/20190905202224/http://kb.mozillazine.org/File_types_and_download_actions
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')
BASE_URL = 'https://national-tv.rentrak.com'

# Create output folder
script_folder = os.getcwd()
output_folder = os.path.join(script_folder, 'output')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Assume that "chromedrive/chromedriver.exe" shares same PARENT folder as this script
parent_folder = os.path.dirname(os.path.normpath(script_folder))
chromedriver_exe_with_path = os.path.join(parent_folder , 'chromedriver', 'chromedriver.exe')
print("\nInvoking Chrome driver at:", chromedriver_exe_with_path, "\n")
browser = webdriver.Chrome(executable_path=chromedriver_exe_with_path)

browser.get(BASE_URL)
browser.find_element_by_id('login_id').clear()
browser.find_element_by_id('password').clear()
browser.find_element_by_id('login_id').send_keys(account_info.USERNAME)
browser.find_element_by_id('password').send_keys(account_info.PASSWORD)
browser.find_element_by_css_selector('input[type=\"submit\"]').click()

# cur_datetime = datetime.now()
# # We have decided to fetch YTD data (January of current year) to (current month of current year)
# # E.g., from '20190101 00:00:00' to '20190901 00:00:00'
# from_date = ''.join([cur_datetime.strftime('%Y'),'0101'])
# to_date = ''.join([cur_datetime.strftime('%Y%m'),'01'])
# from_datetime = ''.join([from_date,' 00:00:00'])
# to_datetime = ''.join([to_date,' 00:00:00'])
#
# # Following bookmarks and filename prefixes are used to download Network Monthly Trends
# bookmarks_filename_prefix = {
#     'DoNotDelete_Automation_Network_Monthly_Trend_A-L_Networks_All_Markets':
#         'Network_Monthly_Trend_A_L_Networks_All_Markets',
#     'DoNotDelete_Automation_Network_Monthly_Trend_M-Z_Networks_All_Markets':
#         'Network_Monthly_Trend_M_Z_Networks_All_Markets'
# }
#
# for b, fp in bookmarks_filename_prefix.items():
#     print("\nProcessing bookmark:", b)
#     bookmark_menu = browser.find_element_by_xpath('//a[contains(text(),\"{0}\")]'.format(b))
#     bookmark_url = bookmark_menu.get_attribute('href')
#     print("\nExtracted bookmark URL:", bookmark_url)
#     browser.get(bookmark_url)
#
#     from_date_option = browser.find_element_by_xpath('//*[@id="simple_month_range_from_select"]/option[contains(@value, "{0}")]'.format(from_datetime))
#     to_date_option = browser.find_element_by_xpath('//*[@id="simple_month_range_to_select"]/option[contains(@value, "{0}")]'.format(to_datetime))
#     from_date_option.click()
#     to_date_option.click()
#
#     # This does not work for below: browser.find_element_by_css_selector('input[name=\"go\"]')
#     go_button = browser.find_element_by_css_selector('.js-load-indicator')
#     go_button.click()
#
#     # We cannot wait explicitly like suggested in the reference below:
#     # REF 1: https://stackoverflow.com/questions/56119289/element-not-interactable-selenium
#     # REF 2: http://web.archive.org/web/20190905194252/https://blog.codeship.com/get-selenium-to-wait-for-page-load/
#     # because we cannot verify if/when the href in Excel button is updated (from the existing one)
#     # REF: https://selenium-python.readthedocs.io/waits.html#explicit-waits (explicit wait)
#     # Thus, wait for about a few seconds before fetching link from Excel button.
#     # Update on Sept 5, 2019: Turns out we don't need to do this wait and the new href is posted almost instantaneously.
#     # browser.implicitly_wait(10)
#
#     excel_download_button = browser.find_element_by_xpath("//*[@title='Download Report to Excel']")
#     excel_download_url = excel_download_button.get_attribute('href')
#     print("\nDownloading excel file from URL:", excel_download_url)
#
#     # We will get the name of the existing latest downloaded file name before we start downloading the new data file
#     existing_latest_file = get_latest_file_in_folder(DOWNLOAD_FOLDER)
#     browser.get(excel_download_url)
#
#     # Let's busy wait until the file is downloaded (no way to detect successful page load via Selenium
#     time_waited_so_far_in_sec = 0
#     while existing_latest_file == get_latest_file_in_folder(DOWNLOAD_FOLDER):
#         time.sleep(WAIT_TIME_INCREMENT_IN_SEC)
#         time_waited_so_far_in_sec += WAIT_TIME_INCREMENT_IN_SEC
#         if time_waited_so_far_in_sec > WAIT_TIME_LIMIT: # if download is taking longer than 5 minutes, break and print error message
#             print("WARNING: It seems to be taking longer than", WAIT_TIME_LIMIT, ". We are skipping download for bookmark:", b)
#             break
#
#     if existing_latest_file != get_latest_file_in_folder(DOWNLOAD_FOLDER):
#         # Rename and move the downloaded file to 'output' folder which is located in the same parent folder as this script
#         # downloaded_filename, downloaded_file_extension = os.path.splitext(downloaded_file_path_and_name)
#         new_file_name = ''.join([fp, '_', from_date, '_', to_date, '.xlsx'])
#         new_file_path_and_name = os.path.join(output_folder, new_file_name)
#         print("\nRenaming and moving downloaded file:", get_latest_file_in_folder(DOWNLOAD_FOLDER),
#               "\tto:", new_file_path_and_name)
#         try:
#             os.rename(get_latest_file_in_folder(DOWNLOAD_FOLDER), new_file_path_and_name)
#         except FileExistsError:
#             os.remove(new_file_path_and_name)
#             os.rename(get_latest_file_in_folder(DOWNLOAD_FOLDER), new_file_path_and_name)
#
# # MONTHLY_MARKET_TREND_URL = '/reports/market_month_trend.html'
# print("\nNetwork Monthly Trend YTD data download finished.")


# cur_datetime = datetime.now()
# from_date = '20160101'#''.join([cur_datetime.strftime('%Y'),'0101'])
# to_date = '201612'#''.join([cur_datetime.strftime('%Y%m'),'01'])
# from_datetime = ''.join([from_date,' 00:00:00'])
# to_datetime = ''.join([to_date,'01 00:00:00'])
#
# # Following bookmarks and filename prefixes are used to download Market Monthly Trends
# bookmarks_filename_prefix = {
#     'DoNotDelete_Automation_Market_Monthly_Trend_Individual_Network_All_Markets':
#         'Market_Monthly_Trend_Individual_Network_All_Markets_'
# }
#
# for b, fp in bookmarks_filename_prefix.items():
#     print("\nProcessing bookmark:", b)
#     bookmark_menu = browser.find_element_by_xpath('//a[contains(text(),\"{0}\")]'.format(b))
#     bookmark_url = bookmark_menu.get_attribute('href')
#     print("\nExtracted bookmark URL:", bookmark_url)
#     browser.get(bookmark_url)
#
#     from_date_option = browser.find_element_by_xpath('//*[@id="simple_month_range_from_select"]/option[contains(@value, "{0}")]'.format(from_datetime))
#     to_date_option = browser.find_element_by_xpath('//*[@id="simple_month_range_to_select"]/option[contains(@value, "{0}")]'.format(to_datetime))
#     from_date_option.click()
#     to_date_option.click()
#
#     network_names = []
#     for network_name_node in browser.find_elements_by_xpath('//ul[@id="network_no_list"]/li/ul/li[1]/ul//child::li'):
#         network_name = network_name_node.find_element_by_xpath('span').get_attribute('innerHTML')
#         network_names.append(network_name)
#
#     print(network_names)
#     sys.exit()
#
#     for network_name in network_names:
#         network_name = correct_ampersand_character(network_name)
#         print("\nGetting data for network:", network_name)
#         # Click on 'Network' drop down menu.
#         # https://stackoverflow.com/a/46220662/1330974
#         browser.find_element_by_css_selector('#custom-network-no-style > span:nth-child(1)').click()
#
#         # Enter network name in the search box.
#         # Note: Turns out there are two input tags and I was stuck for an hour trying to click on the first one,
#         # only to realize later when checking 'is_displayed' that the first one is not visible/interactable.
#         # browser.find_elements_by_xpath('//div[@class="tree-search"]/input')[0].is_displayed()
#         # while (not browser.find_elements_by_xpath('//div[@class="tree-search"]/input')[0].is_displayed()):
#         #     time.sleep(5)
#         #     print("busy waiting")
#         search_box = browser.find_elements_by_xpath('//div[@class="tree-search"]/input[@name="search"]')[1]
#         search_button = browser.find_elements_by_xpath('//div[@class="tree-search"]/input[@name="search_submit"]')[1]
#         search_box.clear()
#         search_box.send_keys(network_name)
#         search_button.click()
#
#         # Choose the network name from the returned search results above.
#         network_menu_option = browser.find_elements_by_xpath('//span[contains(text(), "{0}")]'.format(network_name))[0]
#         network_menu_option.click()
#
#         # Set the configurations by clicking 'Go' button, which triggers to call a new page with relevnant data.
#         go_button = browser.find_element_by_css_selector('.js-load-indicator')
#         go_button.click()
#
#         # Click on 'Excel' button to download Excel data file.
#         excel_download_button = browser.find_element_by_xpath("//*[@title='Download Report to Excel']")
#         excel_download_url = excel_download_button.get_attribute('href')
#         print("\nDownloading excel file from URL:", excel_download_url)
#
#         # We will get the name of the existing latest downloaded file name before we start downloading the new data file
#         existing_latest_file = get_latest_file_in_folder(DOWNLOAD_FOLDER)
#         browser.get(excel_download_url)
#
#         # IMPORTANT ASSUMPTION: here, we don't expect any parallel process to be creating new files within Download folder
#         # while we are running this Rentrak scraping.
#         # Let's busy wait until the file is downloaded (no way to detect successful page load via Selenium
#         time_waited_so_far_in_sec = 0
#         while existing_latest_file == get_latest_file_in_folder(DOWNLOAD_FOLDER):
#             time.sleep(WAIT_TIME_INCREMENT_IN_SEC)
#             time_waited_so_far_in_sec += WAIT_TIME_INCREMENT_IN_SEC
#             if time_waited_so_far_in_sec > WAIT_TIME_LIMIT: # if download is taking longer than 5 minutes, break and print error message
#                 print("WARNING: It seems to be taking longer than", WAIT_TIME_LIMIT, ". We are skipping download for bookmark:", b)
#                 break
#
#         if existing_latest_file != get_latest_file_in_folder(DOWNLOAD_FOLDER):
#             # We need to sanitize some network names like 'BET: Black Entertainment Television' and
#             # 'Cartoon Network/Adult Swim' because '/' and ':' characters aren't allowed as file names
#             # in Windows system
#             sanitized_network_name = sanitize_name(network_name)
#
#             # Rename and move the downloaded file to 'output' folder which is located in the same parent folder as this script
#             # downloaded_filename, downloaded_file_extension = os.path.splitext(downloaded_file_path_and_name)
#             new_file_name = ''.join([fp, '_', from_date, '_', to_date, '__', sanitized_network_name, '.xlsx'])
#             new_file_path_and_name = os.path.join(output_folder, new_file_name)
#             print("\nRenaming and moving downloaded file:", get_latest_file_in_folder(DOWNLOAD_FOLDER),
#                   "\tto:", new_file_path_and_name)
#             try:
#                 os.rename(get_latest_file_in_folder(DOWNLOAD_FOLDER), new_file_path_and_name)
#             except FileExistsError:
#                 os.remove(new_file_path_and_name)
#                 os.rename(get_latest_file_in_folder(DOWNLOAD_FOLDER), new_file_path_and_name)
#
# # MONTHLY_MARKET_TREND_URL = '/reports/market_month_trend.html'
# print("\nMarket Monthly Trend YTD data download finished.")



cur_datetime = datetime.now()
from_date = '20160101'#''.join([cur_datetime.strftime('%Y'),'0101'])
to_date = '20161201'#''.join([cur_datetime.strftime('%Y%m'),'01'])
from_datetime = ''.join([from_date,' 00:00:00'])
to_datetime = ''.join([to_date,' 00:00:00'])

# Following bookmarks and filename prefixes are used to download Market Monthly Trends
bookmarks_filename_prefix = {
    'DoNotDelete_Automation_Market_Monthly_Trend_Individual_Network_All_Markets':
        'Market_Monthly_Trend_Individual_Network_All_Markets_'
}

for b, fp in bookmarks_filename_prefix.items():
    print("\nProcessing bookmark:", b)
    bookmark_menu = browser.find_element_by_xpath('//a[contains(text(),\"{0}\")]'.format(b))
    bookmark_url = bookmark_menu.get_attribute('href')
    print("\nExtracted bookmark URL:", bookmark_url)
    browser.get(bookmark_url)

    from_date_option = browser.find_element_by_xpath('//*[@id="simple_month_range_from_select"]/option[contains(@value, "{0}")]'.format(from_datetime))
    to_date_option = browser.find_element_by_xpath('//*[@id="simple_month_range_to_select"]/option[contains(@value, "{0}")]'.format(to_datetime))
    from_date_option.click()
    to_date_option.click()

    # # Click on 'Network' drop down menu.
    # # https://stackoverflow.com/a/46220662/1330974
    # browser.find_element_by_css_selector('#custom-network-no-style > span:nth-child(1)').click()
    #
    # # Enter network name in the search box.
    # # Note: Turns out there are two input tags and I was stuck for an hour trying to click on the first one,
    # # only to realize later when checking 'is_displayed' that the first one is not visible/interactable.
    # # browser.find_elements_by_xpath('//div[@class="tree-search"]/input')[0].is_displayed()
    # # while (not browser.find_elements_by_xpath('//div[@class="tree-search"]/input')[0].is_displayed()):
    # #     time.sleep(5)
    # #     print("busy waiting")
    # search_box = browser.find_elements_by_xpath('//div[@class="tree-search"]/input[@name="search"]')[1]
    # search_button = browser.find_elements_by_xpath('//div[@class="tree-search"]/input[@name="search_submit"]')[1]
    # search_box.clear()
    # search_box.send_keys(network_name)
    # search_button.click()
    #
    # # Choose the network name from the returned search results above.
    # network_menu_option = browser.find_elements_by_xpath('//span[contains(text(), "{0}")]'.format(network_name))[0]
    # network_menu_option.click()


    # Set the configurations by clicking 'Go' button, which triggers to call a new page with relevnant data.
    # go_button = browser.find_element_by_css_selector('.js-load-indicator')
    # go_button.click()

    network_ids = []
    # Fetch network ID's from the web page so that we can insert them to generate URLs to fetch
    for network_id_node in browser.find_elements_by_xpath('//ul[@id="network_no_list"]/li/ul/li[1]/ul/li/span[@class="v"]'):
        network_id = network_id_node.get_attribute('innerHTML').split('~')[1] # split strings like 'network_no~462'
        network_ids.append(network_id)

    network_names = []
    # This time, we get network names from corresponding nodes (siblings)
    for network_name_node in browser.find_elements_by_xpath('//ul[@id="network_no_list"]/li/ul/li[1]/ul/li/span[@class="v"]/preceding-sibling::span'):
        network_name = network_name_node.get_attribute('innerHTML')
        network_names.append(network_name)

    for n in zip(network_ids, network_names):
        network_id = n[0]
        network_name = correct_ampersand_character(n[1])
        print("\nGetting data for network:", network_name, "\twith id:", network_id)
        s = 'https://national-tv.rentrak.com/reports/market_month_trend.html?dsr_hideshow_hh_rating=hh_rating;dsr_sort_MarketMonthlyTrends=market_name%20broadcast_month;network_no=6018462;simple_month_range=20160101%2000%3A00%3A00;'

        cur_url = re.sub(r';?bookmark_no=\d+','',browser.current_url) # remove 'bookmark_no=...' portion
        cur_url = re.sub(r'network_no=[\d;]+',''.join(['network_no=', network_id, ';']), cur_url) # insert network id in the URL
        cur_url = replace_nth_str(cur_url, 'simple_month_range=20190101', 'simple_month_range=20160101', 1)
        cur_url = replace_nth_str(cur_url, 'simple_month_range=20190101', 'simple_month_range=20161201', 1)
        print("Fetching url:", cur_url)

        browser.get(cur_url)

        # Click on 'Excel' button to download Excel data file.
        excel_download_button = browser.find_element_by_xpath("//*[@title='Download Report to Excel']")
        excel_download_url = excel_download_button.get_attribute('href')
        print("\nDownloading excel file from URL:", excel_download_url)

        # We will get the name of the existing latest downloaded file name before we start downloading the new data file
        existing_latest_file = get_latest_file_in_folder(DOWNLOAD_FOLDER)
        browser.get(excel_download_url)

        # IMPORTANT ASSUMPTION: here, we don't expect any parallel process to be creating new files within Download folder
        # while we are running this Rentrak scraping.
        # Let's busy wait until the file is downloaded (no way to detect successful page load via Selenium
        time_waited_so_far_in_sec = 0
        while existing_latest_file == get_latest_file_in_folder(DOWNLOAD_FOLDER):
            time.sleep(WAIT_TIME_INCREMENT_IN_SEC)
            time_waited_so_far_in_sec += WAIT_TIME_INCREMENT_IN_SEC
            if time_waited_so_far_in_sec > WAIT_TIME_LIMIT: # if download is taking longer than 5 minutes, break and print error message
                print("WARNING: It seems to be taking longer than", WAIT_TIME_LIMIT, ". We are skipping download for bookmark:", b)
                break

        if existing_latest_file != get_latest_file_in_folder(DOWNLOAD_FOLDER):
            # We need to sanitize some network names like 'BET: Black Entertainment Television' and
            # 'Cartoon Network/Adult Swim' because '/' and ':' characters aren't allowed as file names
            # in Windows system
            sanitized_network_name = sanitize_name(network_name)

            # Rename and move the downloaded file to 'output' folder which is located in the same parent folder as this script
            # downloaded_filename, downloaded_file_extension = os.path.splitext(downloaded_file_path_and_name)
            new_file_name = ''.join([fp, '_', from_date, '_', to_date, '__', sanitized_network_name, '.xlsx'])
            new_file_path_and_name = os.path.join(output_folder, new_file_name)
            print("\nRenaming and moving downloaded file:", get_latest_file_in_folder(DOWNLOAD_FOLDER),
                  "\tto:", new_file_path_and_name)
            try:
                os.rename(get_latest_file_in_folder(DOWNLOAD_FOLDER), new_file_path_and_name)
            except FileExistsError:
                os.remove(new_file_path_and_name)
                os.rename(get_latest_file_in_folder(DOWNLOAD_FOLDER), new_file_path_and_name)

        time.sleep(5) # we will be polite and wait 5 seconds between each fetch

browser.close()
print("\nMarket Monthly Trend YTD data download finished.")