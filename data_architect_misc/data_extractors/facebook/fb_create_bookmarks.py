"""
Author: Phyo Thiha
Last Modified Date: September 25, 2019
Description: This is script is used to create bookmarks on Facebook's Business Manager site.
We have ~48 FB accounts and each account has 16 report templates to create, so we will
automate creation of these report templates.

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
from selenium.webdriver.common.keys import Keys
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


def log_in(browser):
    print("Logging into Business Manager.")
    browser.get(account_info.BASE_URL)
    browser.find_element_by_id('email').clear()
    browser.find_element_by_id('pass').clear()
    browser.find_element_by_id('email').send_keys(account_info.USERNAME)
    browser.find_element_by_id('pass').send_keys(account_info.PASSWORD)
    browser.find_element_by_id('loginbutton').click()


def go_to_ads_reporting(browser, ads_reporting_url):
    print("\nFetching Ads Reporting default landing page (to populate/collect links to landing page for each account).")
    browser.get(ads_reporting_url)


def click_xpath(browser, xpath):
    ele = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC)\
        .until(ec.element_to_be_clickable((By.XPATH, xpath)))
    ele.click()
    # We need this because sometimes (e.g., in clicking on 'save' button) is not clickable
    # (although we use 'element_to_be_clickable' above)
    time.sleep(WAIT_TIME_INCREMENT_IN_SEC)


def enter_str_to_input_field(browser, xpath_to_input_field, str_to_enter):
    # REF: https://stackoverflow.com/a/56875177
    # REF: Selenium expected conditions https://selenium-python.readthedocs.io/waits.html
    input_field = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC)\
        .until(ec.element_to_be_clickable((By.XPATH, xpath_to_input_field)))
    input_field.send_keys(Keys.CONTROL + 'a')
    input_field.send_keys(Keys.DELETE)
    input_field.send_keys(str_to_enter)


def check_option_box(browser, option_label):
    button_xpath = '//span[text()="{0}"]/ancestor::label/button'.format(option_label)
    checkbox_btn = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC) \
        .until(ec.presence_of_element_located((By.XPATH, button_xpath)))
    i = 0
    scroll_bar_xpath = '//div[@id="left_rail_nux_target_node"]/div/div'
    scroll_bar = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC) \
        .until(ec.presence_of_element_located((By.XPATH, scroll_bar_xpath)))

    while not checkbox_btn.is_displayed():
        checkbox_location = browser.find_element_by_xpath(button_xpath).location['y'] + i
        js_scroll = ''.join(['arguments[0].scrollTop=', str(checkbox_location), ';'])
        browser.execute_script(js_scroll, scroll_bar)
        # we will scroll 200 pixel every time until the checkbox appears in the visible DOM
        i += 200

    checkbox_btn = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC) \
        .until(ec.element_to_be_clickable((By.XPATH, button_xpath)))
    if checkbox_btn.get_attribute('aria-checked') != 'true':
        print("Box checked:", option_label)
        time.sleep(2)
        # Only click on the checkbox if it has not been checked
        checkbox_btn.click()
        time.sleep(WAIT_TIME_INCREMENT_IN_SEC)
    else:
        print("Box skipped:", option_label)


def get_report_date_range(browser):
    date_range_xpath = '//span[@data-testid="date_picker"]'
    date_range_dropdown = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC)\
        .until(ec.presence_of_element_located((By.XPATH, date_range_xpath)))
    raw_date_str = [d.strip(',') for d in date_range_dropdown.text.split()]
    to_date = ''.join([raw_date_str[-1],
                       datetime.strptime(raw_date_str[-3], '%b').strftime('%m'),
                       datetime.strptime(raw_date_str[-2], '%d').strftime('%d')])
    from_date = ''.join([raw_date_str[-5],
                         datetime.strptime(raw_date_str[-7], '%b').strftime('%m'),
                         datetime.strptime(raw_date_str[-6], '%d').strftime('%d')])
    return (from_date, to_date)


def main():
    folder_that_has_this_code = os.getcwd()
    # Note: Make sure that "chromedrive/chromedriver.exe" shares same PARENT folder as this script
    parent_folder = os.path.dirname(os.path.normpath(folder_that_has_this_code))
    chromedriver_exe_with_path = os.path.join(parent_folder , 'chromedriver', 'chromedriver.exe')
    print("\nInvoking Chrome driver at:", chromedriver_exe_with_path, "\n")
    browser = webdriver.Chrome(executable_path=chromedriver_exe_with_path)

    log_in(browser)
    go_to_ads_reporting(browser, account_info.ADS_REPORTING_URL)

    accounts_dropdown_xpath = '//div[@role="toolbar"]/*/button'
    click_xpath(browser, accounts_dropdown_xpath)

    # Just busy waiting until Account # dropdown is present
    accounts = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC)\
        .until(ec.presence_of_element_located((By.XPATH, '//a[@data-testid="big-ad-account-selector-item"]//*//div[contains(text(),"Account #")]')))

    # Generate URLs that will directly bring us to Ads Report page (otherwise, we'll have to navigate using FB's ever changing web UI)
    report_urls = [''.join(['https://business.facebook.com/adsmanager/reporting/view?',
                              re.search('.*(act.*)', e.get_attribute('href'), re.I)[1]])
                   for e in browser.find_elements_by_xpath('//a[@data-testid="big-ad-account-selector-item"]')]

    # Prepare list of options to choose for 14 different templates we want to build
    breakdowns_options_to_always_include = ['Campaign Name', 'Ad Set Name', 'Ad Name', 'Campaign ID', 'Ad Set ID',
                                            'Ad ID', 'Day', 'Objective']
    breakdowns_options = [
        breakdowns_options_to_always_include + [] + ['Video Sound'],

        breakdowns_options_to_always_include + ['Age', 'Gender'],
        breakdowns_options_to_always_include + ['Age', 'Gender'] + ['Destination'],
        breakdowns_options_to_always_include + ['Age', 'Gender'] + ['Video View Type'],
        breakdowns_options_to_always_include + ['Age', 'Gender'] + ['Carousel Card'],

        breakdowns_options_to_always_include + ['Country'],
        breakdowns_options_to_always_include + ['Country'],
        breakdowns_options_to_always_include + ['Country'],
        breakdowns_options_to_always_include + ['Country'],

        breakdowns_options_to_always_include + ['Impression Device', 'Platform', 'Placement', 'Device Platform'],
        breakdowns_options_to_always_include + ['Impression Device', 'Platform', 'Placement', 'Device Platform'],
        breakdowns_options_to_always_include + ['Impression Device', 'Platform', 'Placement', 'Device Platform'],
        breakdowns_options_to_always_include + ['Impression Device', 'Platform', 'Placement', 'Device Platform'],
        breakdowns_options_to_always_include + ['Impression Device', 'Platform', 'Placement', 'Device Platform'],

        breakdowns_options_to_always_include + ['Product ID'] + ['Destination'],
        breakdowns_options_to_always_include + ['Product ID'] + ['Video View Type']
    ]

    performance_options = ['Results', 'Reach', 'Frequency', 'Impressions', 'Delivery', 'Amount Spent',
                                   'Clicks (All)', 'Cost per Result', 'Cost per 1,000 People Reached',
                                   'CPM (Cost per 1,000 Impressions)', 'Ad Delivery', 'Ad Set Delivery',
                                   'Campaign Delivery']

    # TODO: Starting October 2019, FB will change names of 'Video View' to 'Video Play' in some of the metrics above
    engagement_options = ['Unique 2-Second Continuous Video Views', '2-Second Continuous Video Views',
                          '3-Second Video Views', '10-Second Video Views', 'Unique 10-Second Video Views',
                          'ThruPlays', 'Video Average Watch Time', 'Video Plays',
                          'Cost per 2-Second Continuous Video View', 'Cost per 3-Second Video View',
                          'Cost per 10-Second Video View', 'Cost per ThruPlay', 'CTR (Link Click-Through Rate)',
                          'Estimated Ad Recall Lift (People)', 'Estimated Ad Recall Lift Rate',
                          'Cost per Estimated Ad Recall Lift (People)']
    metrics_setting_options = ['Account ID', 'Account Name', 'Reporting Starts', 'Reporting Ends', 'Bid',
                               'Buying Type', 'Objective', 'Schedule', 'Ad ID', 'Ad Name',
                               'Ad Set ID', 'Ad Set Name', 'Campaign Budget', 'Campaign ID', 'Campaign Name']
    metrics_options_to_always_include = performance_options + engagement_options + metrics_setting_options

    for options in breakdowns_options:
        for url in report_urls:
            print("\nFetching:", url)
            browser.get(url)
            # Wait to load all the elements or we will end up getting account names like 'Loading___'
            time.sleep(WAIT_TIME_INCREMENT_IN_SEC)

            accnt_name_id = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC) \
                .until(ec.presence_of_element_located(
                (By.XPATH, '//div[@role="toolbar"]/*/button/*/div[@data-hover="tooltip"]')))
            accnt_name_str = re.sub(r'\W', '_', accnt_name_id.text)
            print("\nCreating a report template for accnt:", accnt_name_str)

            try:
                create_btn_xpath = '//div[text()="Create"]'
                click_xpath(browser, create_btn_xpath)
            except TimeoutException:
                # This means, we are redirected to 'All Reports' page because this account didn't have any prior report templates created
                print(
                    "No prior report template exists for this account, so we are now in the "
                    "'All Reports' page and we'll be creating new report templates")

            print("with options:", options)
            for option_label in options:
                check_option_box(browser, option_label)

            # Now we switch to Metrics tab
            metrics_tab_xpath = '//ul[@role="tablist"]/li[2]'
            click_xpath(browser, metrics_tab_xpath)
            print("\nSwitching to 'Metrics' tab.")
            for option_label in metrics_options_to_always_include:
                check_option_box(browser, option_label)

            date_picker_xpath = '//span[@data-testid="date_picker"]/parent::div'
            last_week_option_xpath = '//ul[@aria-label="Date range selection menu"]/li[text()="Last week"]'
            click_xpath(browser, date_picker_xpath)
            click_xpath(browser, last_week_option_xpath)

            # Combine strings of accnt_name, breakdowns and date range to form template name
            options_str = '_'.join([re.sub(r'\W', '', i) for i in options])
            from_date, to_date = get_report_date_range(browser)
            template_name = '_'.join(['DoNotDelete', accnt_name_str, options_str, from_date, to_date])

            edit_report_name_xpath = '//a[@id="all_reports_link"]/following-sibling::a[@href="#"]'
            input_field_xpath = '//input[@placeholder="Untitled Report"]'
            report_name_confirm_btn_xpath = '//div[text()="Confirm"]/ancestor::button'
            save_btn_xpath = '//div[@id="save_button"]'  # '//div[@id="save_button"]/div/button'

            click_xpath(browser, edit_report_name_xpath)
            enter_str_to_input_field(browser, input_field_xpath, template_name)
            click_xpath(browser, report_name_confirm_btn_xpath)
            click_xpath(browser, save_btn_xpath)
            print("Created report template:", template_name)
            # TODO:
            # Start from place like this https://www.facebook.com/adsmanager/reporting/manage?act=675301196287656
            # and for every report template under that, click on 'export' and maybe also download for
            # 2016, 2017 so on, by appending '&time_range=2019-01-01_2019-08-31' to
            # bookmarked template URL: https://www.facebook.com/adsmanager/reporting/view?act=675301196287656&selected_report_id=23843815761760384
            # pdb.set_trace()
            # print("aha")



    # browser.close()
    # pdb.set_trace()
    print("\nCreated bookmarks on FB Business Manager website.")


if __name__ == '__main__':
    main()
