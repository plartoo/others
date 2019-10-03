"""
Author: Phyo Thiha
Last Modified Date: October 1, 2019
Description: This is script is used to create report templates on Facebook's Business Manager site.
We have ~48 FB accounts and each account has 16 report templates to create, so we will automate
the creation of these report templates.

Note: For anyone interested, read the following resources to learn more about Selenium:
# Selenium Docs: http://selenium-python.readthedocs.io/
# http://web.archive.org/web/20190830175223/http://thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1/
# http://web.archive.org/web/20190830175349/http://thiagomarzagao.com/2013/11/14/webscraping-with-selenium-part-2/
# http://web.archive.org/web/20190830175411/http://thiagomarzagao.com/2013/11/15/webscraping-with-selenium-part-3/
# http://web.archive.org/web/20190830175437/https://www.scrapehero.com/tutorial-web-scraping-hotel-prices-using-selenium-and-python/
"""

import pdb

from datetime import datetime
import os
import re
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# import account_info
import fb_common


TEMPLATE_LIST_LOG_FILE = 'accnts_with_templates.txt'
# Prepare list of options to choose for 14 different templates we want to build
MUST_HAVE_BREAKDOWN_OPTIONS = ['Account Name', 'Campaign Name', 'Ad Set Name', 'Ad Name',
                               'Account ID', 'Campaign ID', 'Ad Set ID', 'Ad ID', 'Day',
                               'Objective']
BREAKDOWN_OPTIONS = [
    MUST_HAVE_BREAKDOWN_OPTIONS + [] + ['Video Sound'],

    MUST_HAVE_BREAKDOWN_OPTIONS + ['Age', 'Gender'],
    MUST_HAVE_BREAKDOWN_OPTIONS + ['Age', 'Gender'] + ['Destination'],
    MUST_HAVE_BREAKDOWN_OPTIONS + ['Age', 'Gender'] + ['Video View Type'],
    MUST_HAVE_BREAKDOWN_OPTIONS + ['Age', 'Gender'] + ['Carousel Card'],

    MUST_HAVE_BREAKDOWN_OPTIONS + ['Country'],
    MUST_HAVE_BREAKDOWN_OPTIONS + ['Country'] + ['Destination'],
    MUST_HAVE_BREAKDOWN_OPTIONS + ['Country'] + ['Video View Type'],
    MUST_HAVE_BREAKDOWN_OPTIONS + ['Country'] + ['Carousel Card'],

    MUST_HAVE_BREAKDOWN_OPTIONS + ['Impression Device', 'Platform', 'Placement', 'Device Platform'],
    MUST_HAVE_BREAKDOWN_OPTIONS + ['Impression Device', 'Platform', 'Placement', 'Device Platform'] + [
        'Destination'],
    MUST_HAVE_BREAKDOWN_OPTIONS + ['Impression Device', 'Platform', 'Placement', 'Device Platform'] + [
        'Video View Type'],
    MUST_HAVE_BREAKDOWN_OPTIONS + ['Impression Device', 'Platform', 'Placement', 'Device Platform'] + [
        'Carousel Card'],
    MUST_HAVE_BREAKDOWN_OPTIONS + ['Impression Device', 'Platform', 'Placement', 'Device Platform'] + [
        'Conversion Device'],

    MUST_HAVE_BREAKDOWN_OPTIONS + ['Product ID'] + ['Destination'],
    MUST_HAVE_BREAKDOWN_OPTIONS + ['Product ID'] + ['Video View Type']
]

PERFORMANCE_OPTIONS = ['Results', 'Reach', 'Frequency', 'Impressions', 'Delivery', 'Amount Spent',
                       'Clicks (All)', 'Cost per Result', 'Cost per 1,000 People Reached',
                       'CPM (Cost per 1,000 Impressions)', 'Ad Delivery', 'Ad Set Delivery',
                       'Campaign Delivery']

# TODO: Starting October 2019, FB will change names of 'Video View' to 'Video Play' in some of the metrics above
# Note: it's now October 2, but FB hasn't changed the metric names
ENGAGEMENT_OPTIONS = ['Unique 2-Second Continuous Video Views', '2-Second Continuous Video Views',
                      '3-Second Video Views', '10-Second Video Views', 'Unique 10-Second Video Views',
                      'ThruPlays', 'Video Average Watch Time', 'Video Plays',
                      'Cost per 2-Second Continuous Video View', 'Cost per 3-Second Video View',
                      'Cost per 10-Second Video View', 'Cost per ThruPlay', 'CTR (Link Click-Through Rate)',
                      'Estimated Ad Recall Lift (People)', 'Estimated Ad Recall Lift Rate',
                      'Cost per Estimated Ad Recall Lift (People)']

# TODO: Maybe remove 'Account ID' etc. below that are duplicates of MUST_HAVE_BREAKDOWN_OPTIONS
SETTINGS_OPTIONS_IN_METRICS_TAB = ['Account ID', 'Account Name', 'Reporting Starts', 'Reporting Ends', 'Bid',
                                   'Buying Type', 'Objective', 'Schedule', 'Ad ID', 'Ad Name',
                                   'Ad Set ID', 'Ad Set Name', 'Campaign Budget', 'Campaign ID', 'Campaign Name',
                                   'Link (Ad Settings)', 'Currency']
MUST_HAVE_METRICS_OPTIONS = PERFORMANCE_OPTIONS + ENGAGEMENT_OPTIONS + SETTINGS_OPTIONS_IN_METRICS_TAB


def check_option_box(browser, option_label):
    # This method is used to check on the checkbox of *a given option label*
    button_xpath = '//span[text()="{0}"]/ancestor::label/button'.format(option_label)
    checkbox_btn = WebDriverWait(browser, fb_common.WAIT_TIME_IN_SEC) \
        .until(ec.presence_of_element_located((By.XPATH, button_xpath)))

    scroll_bar_xpath = '//div[@id="left_rail_nux_target_node"]/div/div'
    scroll_bar = WebDriverWait(browser, fb_common.WAIT_TIME_IN_SEC) \
        .until(ec.presence_of_element_located((By.XPATH, scroll_bar_xpath)))
    i = 0
    while not checkbox_btn.is_displayed():
        checkbox_location = browser.find_element_by_xpath(button_xpath).location['y'] + i
        js_scroll = ''.join(['arguments[0].scrollTop=', str(checkbox_location), ';'])
        browser.execute_script(js_scroll, scroll_bar)
        # we will scroll 200 pixel every time until the checkbox appears in the visible DOM
        i += 200

    checkbox_btn = WebDriverWait(browser, fb_common.WAIT_TIME_IN_SEC) \
        .until(ec.element_to_be_clickable((By.XPATH, button_xpath)))
    if checkbox_btn.get_attribute('aria-checked') != 'true':
        print("Box checked:", option_label)
        time.sleep(2)
        # Only click on the checkbox if it has not been checked
        checkbox_btn.click()
        time.sleep(fb_common.WAIT_TIME_IN_SEC)
    else:
        print("Box skipped:", option_label)


def click_option_boxes(browser, option_labels, check_or_uncheck):
    if check_or_uncheck not in {"check", "uncheck"}:
        raise ValueError("Choose either 'check' or 'uncheck' as value for clicking option boxes.")

    checkboxes_xpath = '//button[@role="checkbox"]/following-sibling::span/div/span'
    WebDriverWait(browser, fb_common.WAIT_TIME_IN_SEC) \
        .until(ec.presence_of_element_located((By.XPATH, checkboxes_xpath)))
    scrollbar_xpath = '//div[@id="left_rail_nux_target_node"]/div/div'

    for checkbox in browser.find_elements_by_xpath(checkboxes_xpath):
        checkbox_label = checkbox.get_attribute('innerHTML').strip()
        checkbox_button_xpath = '//span[text()="{0}"]/ancestor::label/button'.format(checkbox_label)
        fb_common.scroll_to_element(browser, checkbox_button_xpath, scrollbar_xpath)
        checkbox_button = WebDriverWait(browser, fb_common.WAIT_TIME_IN_SEC) \
            .until(ec.presence_of_element_located((By.XPATH, checkbox_button_xpath)))
        if checkbox_label in option_labels:
            if check_or_uncheck == "check":
                if checkbox_button.get_attribute('aria-checked') != 'true':
                    print("Checking box for:", checkbox_label)
                    checkbox_button.click()
                    time.sleep(fb_common.WAIT_TIME_IN_SEC)
                else:
                    print("Box already checked:", checkbox_label)
            else:
                if checkbox_button.get_attribute('aria-checked') == 'true':
                    print("Unchecking box for:", checkbox_label)
                    checkbox_button.click()
                    time.sleep(fb_common.WAIT_TIME_IN_SEC)
                else:
                    print("Box already unchecked:", checkbox_label)
        else:
            print("Skipping box for:", checkbox_label)
            if checkbox_button.get_attribute('aria-checked') == 'true':
                # If the box is checked, but we don't need this option, uncheck the box
                # Note, this 'if' branch is really not necessary, but I added this here as extra caution
                print("**We don't need this option above, but it's checked, so we are unchecking it.")
                checkbox_button.click()
                time.sleep(fb_common.WAIT_TIME_IN_SEC)


def get_accounts_with_templates_created():
    print("Loading the list of accounts that already have templates created.")
    log_folder = fb_common.create_output_folder(os.getcwd(), 'log')
    template_log_file = os.path.join(log_folder, TEMPLATE_LIST_LOG_FILE)

    accnts_with_templates_created = []
    if os.path.exists(template_log_file):
        with open(template_log_file) as f:
            accnts_with_templates_created = [line.strip() for line in f]
    return accnts_with_templates_created


def log_finished_account_name(account_name):
    print("Logging the name of account we have created templates for:", account_name)
    log_folder = fb_common.create_output_folder(os.getcwd(), 'log')
    template_log_file = os.path.join(log_folder, TEMPLATE_LIST_LOG_FILE)

    with open(template_log_file, 'a') as f:
        f.write(''.join([account_name, '\n']))


def get_all_account_names_and_ids(browser):
    # Fetch account names and ids from the 'Create Report' prompt
    account_checkbox_xpath = '//div[@class="uiScrollableAreaContent"]/div/ul/li'
    WebDriverWait(browser, fb_common.WAIT_TIME_IN_SEC) \
        .until(ec.element_to_be_clickable((By.XPATH, account_checkbox_xpath)))
    account_names = [ele.text.split('\n')[0].strip() for ele in
            browser.find_elements_by_xpath('//div[@class="uiScrollableAreaContent"]/div/ul/li')[1:]]
    account_ids = [ele.text.split('\n')[1].strip() for ele in
            browser.find_elements_by_xpath('//div[@class="uiScrollableAreaContent"]/div/ul/li')[1:]]
    return account_names, account_ids


def main():
    accounts_with_templates = get_accounts_with_templates_created()
    browser = fb_common.get_chrome_browser_instance()
    fb_common.log_in(browser)
    fb_common.go_to_ads_reporting(browser)
    print("\nFetching Ads Reporting default landing page (to collect names of all accounts).")
    time.sleep(fb_common.WAIT_TIME_IN_SEC)

    create_report_btn_xpath = '//div[contains(text(),"Create Report")]//parent::div/parent::button'
    fb_common.click_xpath(browser, create_report_btn_xpath)

    account_names, account_ids = get_all_account_names_and_ids(browser)
    accounts_to_process = list(account_names)
    accounts_to_process = [a for a in account_names if not a in accounts_with_templates or accounts_to_process.remove(a)]
    accnt_search_box_xpath = '//input[@placeholder="Search by account name or ID"]'
    accnt_checkbox_xpath = '//div[@class="uiScrollableAreaContent"]/div/ul/li[1]'
    create_btn_xpath = '//div[text()="Create"]/parent::div/parent::button'

    for cur_account_name in accounts_to_process:
        print("\nCreating a report template for account:", cur_account_name)
        print("Fetching Ads Reporting default landing page (to go to 'Create Report'.")
        fb_common.go_to_ads_reporting(browser)
        time.sleep(fb_common.WAIT_TIME_IN_SEC)

        print("Searching for account in 'Create Report' prompt.")
        fb_common.click_xpath(browser, create_report_btn_xpath)
        # ASSUMPTION: here we (reasonably) hope that there are not duplicates in account names
        fb_common.enter_str_to_input_field(browser, accnt_search_box_xpath, cur_account_name)
        time.sleep(fb_common.WAIT_TIME_IN_SEC)
        fb_common.click_xpath(browser, accnt_checkbox_xpath)

        print("Clicking 'Create Report' button.")
        fb_common.click_xpath(browser, create_btn_xpath)
        time.sleep(fb_common.WAIT_TIME_IN_SEC)

        # Choose date range
        print("Choosing date range for report template.")
        date_picker_xpath = '//span[@data-testid="date_picker"]//button'
        last_week_option_xpath = '//ul[@aria-label="Date range selection menu"]/li[text()="Last week"]'
        fb_common.click_xpath(browser, date_picker_xpath)
        fb_common.click_xpath(browser, last_week_option_xpath)

        # Switch to Metrics tab first because it's common across all different reports we will build
        print("Switching to 'Metrics' tab to check options.")
        metrics_tab_xpath = '//ul[@role="tablist"]/li[2]'
        fb_common.click_xpath(browser, metrics_tab_xpath)
        time.sleep(fb_common.WAIT_TIME_IN_SEC)
        click_option_boxes(browser, MUST_HAVE_METRICS_OPTIONS, "check")

        print("Switching to 'Breakdowns' tab to check options.")
        breakdown_tab_xpath = '//ul[@role="tablist"]/li[1]'
        fb_common.click_xpath(browser, breakdown_tab_xpath)
        time.sleep(fb_common.WAIT_TIME_IN_SEC)

        for i, options in enumerate(BREAKDOWN_OPTIONS):
            print("Checking breakdown options:", options)
            click_option_boxes(browser, options, "check")

            print("Clicking 'Save As' from dropdown menu.")
            save_dropdown_xpath = '//div[@id="save_button"]//button[@data-testid="SUIAbstractMenu/button"]'
            save_as_btn_xpath = '//li[contains(text(), "Save as")]'
            fb_common.click_xpath(browser, save_dropdown_xpath)
            time.sleep(2)
            fb_common.click_xpath(browser, save_as_btn_xpath)
            time.sleep(2)

            # Combine strings of accnt_name, breakdowns and date range to form template name
            print("Entering report name to input field.")
            # from_date, to_date = fb_common.get_report_date_range(browser)
            options_str = '_'.join([re.sub(r'\W', '', i) for i in options])
            template_name = '_'.join([str(i), 'DoNotDelete', cur_account_name, options_str, 'LastWeek'])#from_date, to_date])
            input_field_xpath = '//input[@placeholder="Untitled Report"]'
            fb_common.enter_str_to_input_field(browser, input_field_xpath, template_name)
            time.sleep(2)

            print("Saving report template:", template_name)
            # There are two 'Save As' buttons and we need to make sure we are clicking on the right one
            report_save_btn_xpath = '//div[@aria-label="Save Report As"]//div[text()="Save"]/ancestor::button'
            fb_common.click_xpath(browser, report_save_btn_xpath)
            time.sleep(2)

            print("Unchecking previously selected breakdown options.")
            scrollbar_xpath = '//div[@id="left_rail_nux_target_node"]/div/div'
            # fb_common.scroll_all_the_way_up(browser, scrollbar_xpath)
            click_option_boxes(browser, options, "uncheck")
            print("\n")


        log_finished_account_name(cur_account_name)

    browser.close()
    print("\nCreated bookmarks on FB Business Manager website.")


if __name__ == '__main__':
    main()
