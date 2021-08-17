"""
Last Modified Date: August 15, 2021

Script to scrape medical residency program
information from Sarthi program's website.
You need to have an account with them in
order to use this script. Enter your account
info in the constants 'U' and 'P' below before
running this script.
"""
import os
from datetime import datetime
import re
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By


# IMPORTANT: Must provide account info in the constants below
U = 'ENTER YOUR USERNAME HERE'
P = 'ENTER YOUR PASSWORD HERE'

# IMPORTANT: Because Sarthi site slows down the fetch significantly after
# 100 pages or so, we need to fetch programs in chunk.
# Type the name of the latest fetched program file below
# to continue from the last program fetched.
# If no previous file exists, set the constant to None.
PREVIOUSLY_FETCHED_PROGRAM_DATA_FILE = None

# As of Aug 15, 2021, there are 387 under 'Best Matches' tab.
# NUM_OF_PROGRAMS_TO_FETCH = 400
BASE_URL = 'https://residencymatch.usmlesarthi.com/sarthilist'

FILE_NAME_PREFIX = 'sarthi_fm_programs'

# Time to wait between checking latest downloaded files in 'Download' folder
WAIT_TIME_IN_SEC = 5


def get_chrome_browser_instance():
    folder_that_has_this_code = os.getcwd()
    # Note: Make sure that "chromedrive/chromedriver.exe" shares the same folder as this script
    chromedriver_exe_with_path = os.path.join(folder_that_has_this_code,
                                              'chromedriver.exe')
    print("\nInvoking Chrome driver at:", chromedriver_exe_with_path, "\n")
    return webdriver.Chrome(executable_path=chromedriver_exe_with_path)


def get_program_names_already_fetched(file):
    df = pd.read_csv(file)
    return set(df.Name)


def get_CSV_file_name(file_prefix):
    # Returns file_prefix + date_time_suffix + '.csv' as string
    datetime_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
    return ''.join([
        '_'.join([file_prefix, datetime_suffix])
        , '.csv'])


def scrape_program_details(browser):
    print("\nLogging into the site.")
    browser.get(BASE_URL)
    u_ele = WebDriverWait(browser, 60, 1).until(
        expect.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Username']")))
    p_ele = WebDriverWait(browser, 60, 1).until(
        expect.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Password']")))
    login_ele = WebDriverWait(browser, 60, 1).until(
        expect.visibility_of_element_located(
            (By.XPATH, "//input[@value='Login']")))

    u_ele.send_keys(U)
    p_ele.send_keys(P)
    login_ele.click()
    time.sleep(WAIT_TIME_IN_SEC)

    program_list = []

    if PREVIOUSLY_FETCHED_PROGRAM_DATA_FILE:
        programs_fetched = get_program_names_already_fetched(PREVIOUSLY_FETCHED_PROGRAM_DATA_FILE)
    else:
        programs_fetched = set()

    while True:  # len(programs_fetched) < NUM_OF_PROGRAMS_TO_FETCH:
        program_details = {}

        # Find 'Sarthi List' button and click
        # First, wait until the desired divs are loaded in the browser
        desired_menu_options = WebDriverWait(browser, 60, 1).until(
            expect.visibility_of_element_located(
                (By.XPATH, "//div/*/h6/../parent::div")))
        menu_eles = browser.find_elements_by_xpath("//div/*/h6/../parent::div")
        menu_labels = [h.text for h in menu_eles]
        button_index = [i for i, item in enumerate(menu_labels) if re.search('sarthi list', item, re.I)]
        menu_eles[button_index[0]].click()

        # Find 'Internal Medicine' button and click
        # Wait until the desired divs are loaded in the browser
        desired_menu_options = WebDriverWait(browser, 60, 1).until(
            expect.visibility_of_element_located(
                (By.XPATH, "//div/*/h5/../../parent::div")))
        menu_eles = browser.find_elements_by_xpath("//div/*/h5/../../parent::div")
        menu_labels = [h.text for h in menu_eles]
        button_index = [i for i, item in enumerate(menu_labels) if re.search('family medicine', item, re.I)]
        menu_eles[button_index[0]].click()

        # Scrape names of programs and 'View Details' buttons
        program_table_xpath = "//tr[@class='ng-star-inserted']"
        desired_table_values = WebDriverWait(browser, 60, 1).until(
            expect.visibility_of_element_located(
                (By.XPATH, program_table_xpath)))
        program_table_eles = browser.find_elements_by_xpath(program_table_xpath)

        # Because Sarthi site bringing us all the way back to 'Sarthi List' page,
        # we need to keep a local cache of fetched programs and see if the current
        # element is already fetched. Proceed with the rest ONLY IF it is not fetched.
        td_eles = None
        count = 0
        for tr in program_table_eles[260:]:
            program_name = tr.find_elements_by_tag_name('td')[1].text
            if program_name not in programs_fetched:
                print(f"==>Will fetch program: {program_name}")
                td_eles = tr.find_elements_by_tag_name('td')
                break
            else:
                count = count + 1
                print(f"{count}. Program already fetched: {program_name}")

        if td_eles:
            program_details['Num'] = td_eles[0].text
            program_details['Name'] = td_eles[1].text
            program_details['City'] = td_eles[2].text
            program_details['State'] = td_eles[3].text

            # After clicking on Program Detail page, we scrape the details
            tr.find_element_by_tag_name('button').click()
            detail_pg_xpath = "//tbody[@id='table1']/tr/td"
            desired_table_values = WebDriverWait(browser, 60, 1).until(
                expect.visibility_of_element_located(
                    (By.XPATH, detail_pg_xpath)))
            program_details['Program Type'] = browser.find_elements_by_xpath(detail_pg_xpath)[4].text
            program_details['YoG'] = browser.find_elements_by_xpath(detail_pg_xpath)[5].text
            program_details['IMG Percentage'] = browser.find_elements_by_xpath(detail_pg_xpath)[7].text
            program_details['Last Updated'] = browser.find_elements_by_xpath(detail_pg_xpath)[8].text

            for id in ['Frieda', 'nonUsImgPercentage', 'imgpercentageComments', 'FirstYearSpots',
                       'FirstYearSpotsPrelim']:
                detail_row_xpath = f"//tr[@id='{id}']/td"
                detail_row_eles = browser.find_elements_by_xpath(detail_row_xpath)
                key = detail_row_eles[0].text
                val = detail_row_eles[-1].text
                program_details[key] = val
            print("Scraped basic information from the program detail page.")

            print("Clicked Score Information tab.")
            score_info_tab_xpath = "//li/a[text()='Score Information']"
            score_info_tab_ele = WebDriverWait(browser, 60, 1).until(
                expect.visibility_of_element_located(
                    (By.XPATH, score_info_tab_xpath)))
            browser.find_element_by_xpath(score_info_tab_xpath).click()
            for id in ['Step1Req', 'Step1ScoreLastYearMin', 'Step1ScoreLastYearMax',
                       'Step2Req', 'Step2Min', 'Step2Max', 'Step2Accept',
                       'Step3Accept', 'USMLEExamComments']:
                detail_row_xpath = f"//tr[@id='{id}']/td"
                detail_row_eles = browser.find_elements_by_xpath(detail_row_xpath)
                key = detail_row_eles[0].text
                val = detail_row_eles[-1].text
                program_details[key] = val
            print("Scraped score information from the program detail page.")

            print("Clicked Additional Information tab.")
            additional_info_tab_xpath = "//li/a[text()='Additional Information']"
            additional_info_tab_ele = WebDriverWait(browser, 60, 1).until(
                expect.visibility_of_element_located(
                    (By.XPATH, additional_info_tab_xpath)))
            browser.find_element_by_xpath(additional_info_tab_xpath).click()
            for id in ['DirName', 'DirEmail', 'CorName', 'CorEmail', 'CorPhone', 'website', 'notes']:
                detail_row_xpath = f"//tr[@id='{id}']/td"
                detail_row_eles = browser.find_elements_by_xpath(detail_row_xpath)
                key = detail_row_eles[0].text
                val = detail_row_eles[-1].text
                program_details[key] = val
            print("Scraped additional information from the program detail page.")
            print(program_details)

            program_list.append(program_details)
            programs_fetched.add(program_name)
            program_df = pd.DataFrame.from_records(program_list)
            program_df.to_csv(get_CSV_file_name(FILE_NAME_PREFIX),
                              index=False)
            browser.back()
            time.sleep(3)
        else:
            break

    print(f"Finished fetching this many programs: {len(programs_fetched)}")
    return pd.DataFrame.from_records(program_list)


def main():
    browser = get_chrome_browser_instance()
    program_df = scrape_program_details(browser)
    output_file_name = get_CSV_file_name(FILE_NAME_PREFIX)
    print(f"Wrote fetched program details to this file: {output_file_name}")
    program_df.to_csv(output_file_name,
                      index=False)


if __name__ == '__main__':
    main()
