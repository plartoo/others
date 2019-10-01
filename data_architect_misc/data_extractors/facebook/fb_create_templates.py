"""
Author: Phyo Thiha
Last Modified Date: September 26, 2019
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


def enter_str_to_input_field(browser, xpath_to_input_field, str_to_enter):
    # REF: https://stackoverflow.com/a/56875177
    # REF: Selenium expected conditions https://selenium-python.readthedocs.io/waits.html
    input_field = WebDriverWait(browser, fb_common.WAIT_TIME_IN_SEC)\
        .until(ec.element_to_be_clickable((By.XPATH, xpath_to_input_field)))
    input_field.send_keys(Keys.CONTROL + 'a')
    input_field.send_keys(Keys.DELETE)
    input_field.send_keys(str_to_enter)


def check_option_box(browser, option_label):
    button_xpath = '//span[text()="{0}"]/ancestor::label/button'.format(option_label)
    checkbox_btn = WebDriverWait(browser, fb_common.WAIT_TIME_IN_SEC) \
        .until(ec.presence_of_element_located((By.XPATH, button_xpath)))
    i = 0
    scroll_bar_xpath = '//div[@id="left_rail_nux_target_node"]/div/div'
    scroll_bar = WebDriverWait(browser, fb_common.WAIT_TIME_IN_SEC) \
        .until(ec.presence_of_element_located((By.XPATH, scroll_bar_xpath)))

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


def main():
    browser = fb_common.get_chrome_browser_instance()
    fb_common.log_in(browser)
    fb_common.go_to_ads_reporting(browser, account_info.ADS_REPORTING_URL)
    report_urls = fb_common.get_urls_of_all_accounts(browser,
                                                     'https://business.facebook.com/adsmanager/reporting/view?')

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
        breakdowns_options_to_always_include + ['Country'] + ['Destination'],
        breakdowns_options_to_always_include + ['Country'] + ['Video View Type'],
        breakdowns_options_to_always_include + ['Country'] + ['Carousel Card'],

        breakdowns_options_to_always_include + ['Impression Device', 'Platform', 'Placement', 'Device Platform'],
        breakdowns_options_to_always_include + ['Impression Device', 'Platform', 'Placement', 'Device Platform'] + ['Destination'],
        breakdowns_options_to_always_include + ['Impression Device', 'Platform', 'Placement', 'Device Platform'] + ['Video View Type'],
        breakdowns_options_to_always_include + ['Impression Device', 'Platform', 'Placement', 'Device Platform'] + ['Carousel Card'],
        breakdowns_options_to_always_include + ['Impression Device', 'Platform', 'Placement', 'Device Platform'] + ['Conversion Device'],

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

    for url in report_urls:
        for options in breakdowns_options:
            print("\nFetching:", url)
            browser.get(url)
            # Wait to load all the elements or we will end up getting account names like 'Loading___'
            time.sleep(fb_common.WAIT_TIME_IN_SEC)

            accnt_name_str = fb_common.get_account_name_and_id(browser)
            try:
                print("\nCreating a report template for accnt:", accnt_name_str)
                create_btn_xpath = '//div[text()="Create"]'
                fb_common.click_xpath(browser, create_btn_xpath)
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
            fb_common.click_xpath(browser, metrics_tab_xpath)
            print("\nSwitching to 'Metrics' tab.")
            for option_label in metrics_options_to_always_include:
                check_option_box(browser, option_label)

            date_picker_xpath = '//span[@data-testid="date_picker"]/parent::div'
            last_week_option_xpath = '//ul[@aria-label="Date range selection menu"]/li[text()="Last week"]'
            fb_common.click_xpath(browser, date_picker_xpath)
            fb_common.click_xpath(browser, last_week_option_xpath)

            # Combine strings of accnt_name, breakdowns and date range to form template name
            options_str = '_'.join([re.sub(r'\W', '', i) for i in options])
            from_date, to_date = fb_common.get_report_date_range(browser)
            # TODO: number the reports
            template_name = '_'.join(['DoNotDelete', accnt_name_str, options_str, from_date, to_date])

            edit_report_name_xpath = '//a[@id="all_reports_link"]/following-sibling::a[@href="#"]'
            input_field_xpath = '//input[@placeholder="Untitled Report"]'
            report_name_confirm_btn_xpath = '//div[text()="Confirm"]/ancestor::button'
            save_btn_xpath = '//div[@id="save_button"]'  # '//div[@id="save_button"]/div/button'

            fb_common.click_xpath(browser, edit_report_name_xpath)
            enter_str_to_input_field(browser, input_field_xpath, template_name)
            fb_common.click_xpath(browser, report_name_confirm_btn_xpath)
            fb_common.click_xpath(browser, save_btn_xpath)
            print("Created report template:", template_name)

    browser.close()
    print("\nCreated bookmarks on FB Business Manager website.")


if __name__ == '__main__':
    main()
