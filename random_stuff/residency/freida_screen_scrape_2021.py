"""
Last Modified Date: September 25, 2021

Script to scrape medical residency program
information from Freida website.
"""

import os
from datetime import datetime
import re
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By


INPUT_FILE_WITH_PROGRAM_ID = 'Applied_Program_IDs_from_MyERAS.xlsx'
OUTPUT_FILE_NAME_PREFIX = 'frieda_programs'

BASE_URL = 'https://freida.ama-assn.org/'


def get_chrome_browser_instance():
    folder_that_has_this_code = os.getcwd()
    # Note: Make sure that "chromedrive/chromedriver.exe" shares the same folder as this script
    chromedriver_exe_with_path = os.path.join(folder_that_has_this_code,
                                              'chromedriver.exe')

    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })

    print("\nInvoking Chrome driver at:", chromedriver_exe_with_path, "\n")
    return webdriver.Chrome(executable_path=chromedriver_exe_with_path,
                            chrome_options=option)


def get_program_ids(file_name):
    df = pd.read_excel(file_name)
    return df['Accreditation_IDs'].tolist()


def get_program_names_already_fetched(file):
    df = pd.read_csv(file)
    return set(df.Name)


def get_CSV_file_name(file_prefix):
    # Returns file_prefix + date_time_suffix + '.csv' as string
    datetime_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
    return ''.join([
        '_'.join([file_prefix, datetime_suffix])
        , '.csv'])


def scrape_program_details(program_ids):
    programs = pd.DataFrame()
    i = 0
    for pid in program_ids[205:]:
        print(f"Program ID: {pid}")
        i += 1
        browser = get_chrome_browser_instance()
        browser.get(BASE_URL)
        time.sleep(3)

        search_box_ele = browser.find_elements_by_xpath("//div[@class='freida-typeahead-container__main']/input")[1]
        search_box_ele.send_keys(pid)

        # browser.find_elements_by_xpath("//div[@role='listbox']/ul/li")[0]
        first_result_ele = WebDriverWait(browser, 60, 1).until(expect.visibility_of_element_located(
            (By.XPATH, "//div[@role='listbox']/ul/li")))
        first_result_ele.click()

        no_thanks_ele = WebDriverWait(browser, 60, 1).until(expect.visibility_of_element_located(
            (By.XPATH, "//button/div[text()=\"No thanks, I'll just peek\"]")))
        no_thanks_ele.click()

        prog_name_ele = browser.find_elements_by_xpath("//div[@class='details__title']")
        prog_loc_ele = browser.find_elements_by_xpath("//div[@class='details__location ng-star-inserted']")
        last_updated_ele = browser.find_elements_by_xpath("//div[@class='survey-info']/div[1]")
        survey_info_ele = browser.find_elements_by_xpath("//div[@class='survey-info']/div[2]")

        program = {'ID': pid}

        if not prog_name_ele:
            program['Program_Name'] = 'Not Available'
        else:
            program['Program_Name'] = prog_name_ele[0].text

        if not prog_loc_ele:
            program['Location'] = 'Not Available'
        else:
            program['Location'] = prog_loc_ele[0].text

        if not last_updated_ele:
            program['Last_Updated'] = 'Not Available'
        else:
            program['Last_Updated'] = last_updated_ele[0].text

        if not survey_info_ele:
            program['Survey_Received'] = 'Not Available'
        else:
            program['Survey_Received'] = survey_info_ele[0].text

        program['Contacts'] = []

        for j, contact_ele in enumerate(browser.find_elements_by_xpath("//div[@class='contact-info__contacts ng-star-inserted']/*[1]")):
            detail_contact_info = browser.find_elements_by_xpath("//div[@class='contact-info__contacts ng-star-inserted']/*[1]/following-sibling::small")[j].text
            program_details = {}
            role = contact_ele.text

            if not re.findall(r'(^.*?)\n',detail_contact_info):
                name = 'Not Available'
            else:
                name = re.findall(r'(^.*?)\n',detail_contact_info)[0]

            if not re.findall(r'E-mail: (.*?)$', detail_contact_info):
                email = 'Not Available'
            else:
                email = re.findall(r'E-mail: (.*?)$', detail_contact_info)[0]

            if not re.findall(r'Tel: (.*?)\n', detail_contact_info):
                telephone = 'Not Available'
            else:
                telephone = re.findall(r'Tel: (.*?)\n', detail_contact_info)[0]

            program_details['Role'] = role
            program_details['Name'] = name
            program_details['Email'] = email
            program_details['Phone'] = telephone

            program['Contacts'].append(program_details)

        cur_prog_df = pd.json_normalize(program,
                                        record_path=['Contacts'],
                                        meta=['ID', 'Program_Name', 'Location', 'Last_Updated', 'Survey_Received'])
        programs = pd.concat([programs, cur_prog_df])

        output_file_name = ''.join([OUTPUT_FILE_NAME_PREFIX, '_', str(i), '.xlsx'])
        programs.to_excel(output_file_name, index=False)
        print(programs)
        browser.close()


def main():
    program_ids = get_program_ids(INPUT_FILE_WITH_PROGRAM_ID)
    scrape_program_details(program_ids)


if __name__ == '__main__':
    main()
