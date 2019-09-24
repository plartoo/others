"""
Author: Phyo Thiha
Last Modified Date: September 21, 2019
Description: Script to get puzzles from an online interview site.
"""
import pdb

from datetime import datetime
import json
import os
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
FULL_WINDOW_PIXEL_HEIGHT = 700

DOWNLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')



def create_output_folder(folder_that_has_this_code):
    # Create output folder
    output_folder = os.path.join(folder_that_has_this_code, 'puzzles_output')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder


def log_in(browser):
    username_ele = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC).until(ec.presence_of_element_located((By.XPATH, '//input[@name="login"]')))
    pwd_ele = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC).until(ec.presence_of_element_located((By.XPATH, '//input[@name="password"]'))) #browser.find_element_by_xpath('//input[@name="password"]')
    sign_in_ele = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/button/div')))
    username_ele.clear()
    username_ele.send_keys(account_info.USERNAME)
    pwd_ele.clear()
    pwd_ele.send_keys(account_info.PWD)
    sign_in_ele.click()


def select_show_all_problems(browser):
    all_button = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC).until(ec.presence_of_element_located((By.XPATH, '//select/option[contains(text(),"all")]')))
    all_button.click()


def get_all_problems(browser):
    problem_names_and_urls = []
    # /html/body/div[1]/div[3]/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/table/tbody[1]/tr[1]/td[3]/div/a
    for prob in browser.find_elements_by_xpath('//tbody[@class="reactable-data"]/tr/td/div/a'):
        problem_names_and_urls.append([prob.text, prob.get_attribute('href')])
    return problem_names_and_urls


def click_on_problem_description(browser):
    prob_desc = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC).until(ec.presence_of_element_located((By.XPATH, '//div[contains(@class,"question-content")]')))
    prob_desc.click()


def get_comapnies_and_asked_frequencies(browser):
    # more_btn = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC).until(ec.presence_of_element_located((By.XPATH,
    #                 '//div[contains(@class,"company-tag-wrapper")]/parent::div/div[contains(@class, "show-more-wrapper")]')))
    # more_btn.click()
    #WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC).until(ec.presence_of_element_located((By.XPATH,'//div[contains(@class,"company-tag-wrapper")]/a')))
    company_eles = browser.find_elements_by_xpath('//div[contains(@class,"company-tag-wrapper")]/a')
    companies_frequency = []
    for ce in company_eles:
        companies_frequency.append(ce.get_attribute('text').split('|'))
    return companies_frequency


def get_related_topics(browser):
    related_topics_eles = browser.find_elements_by_xpath('//div[contains(text(), "Related Topics")]/parent::div/parent::div/following-sibling::div/a/span')
    related_topics = []
    for rt in related_topics_eles:
        related_topics.append(rt.get_attribute('innerHTML'))
    return related_topics


def get_similar_questions(browser):
    similar_questions_eles = browser.find_elements_by_xpath('//div[contains(text(), "Similar Questions")]/parent::div/parent::div/following-sibling::div/div/a')
    similar_questions = []
    for s in similar_questions_eles:
        similar_questions.append(s.get_attribute('innerHTML'))
    return similar_questions


def save_problem_desc_screenshot(browser, screenshot_file):
    prob_desc = browser.find_element_by_xpath('//div[contains(@class, "question-content")]')
    prob_desc.screenshot(screenshot_file)


def click_on_solution_tab(browser):
    try:
        soln_tab_ele = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC).until(
            ec.element_to_be_clickable((By.XPATH, '//div[@data-key="solution"]')))# '//span[contains(text(), "Solution")]')))
        time.sleep(3)
        soln_tab_ele.click()
    except ElementClickInterceptedException:
        soln_tab_ele = WebDriverWait(browser, WAIT_TIME_INCREMENT_IN_SEC).until(
            ec.presence_of_element_located((By.XPATH, '//div[@data-key="solution"]')))# '//span[contains(text(), "Solution")]')))
        time.sleep(3)
        soln_tab_ele.click()


def take_solution_screenshot(browser, screenshot_cnt, output_folder, prob_difficulty, prob_name):
    cur_soln_screenshot = os.path.join(output_folder,
                                       ''.join([prob_difficulty, '_', prob_name, '_soln_', str(screenshot_cnt),
                                                '_', datetime.now().strftime('%Y%m%d'), '.png']))
    print("Taking screenshot#:", str(screenshot_cnt))
    browser.save_screenshot(cur_soln_screenshot)


def sanitize_name(name):
    # Replace characters "/ \ ? < > " * | :" that are not valid for file names in Windows (and '/' for Mac and Unix)
    # Then replaces double space characters to single space character for aesthetic reason
    # Example networks that need this:
    # ['A&amp;E', 'Azteca (Broadcast)', 'Azteca (Cable)', 'BET: Black Entertainment Television',
    # 'Cartoon Network/Adult Swim', 'De Película', 'E! - Entertainment Television', "God's Learning Channel",
    # 'Hallmark Movies &amp; Mysteries', 'History Channel en Español', 'Nickelodeon/Nick-at-Nite',
    # 'TV Land/TV Land Classic', 'Utilisima - TV / Canal', 'V-me TV (Cable)']
    return re.sub(r'\s+', ' ', re.sub(r'[\\\/\?<>\"\*|:]', ' ', name))


def main():
    folder_that_has_this_code = os.getcwd()
    output_folder = create_output_folder(folder_that_has_this_code)

    # Assume that "chromedrive/chromedriver.exe" shares same PARENT folder as this script
    parent_folder = os.path.dirname(os.path.normpath(folder_that_has_this_code))
    chromedriver_exe_with_path = os.path.join(parent_folder , 'chromedriver', 'chromedriver.exe')
    print("\nInvoking Chrome driver at:", chromedriver_exe_with_path, "\n")
    browser = webdriver.Chrome(executable_path=chromedriver_exe_with_path)
    browser.maximize_window()
    browser.get(account_info.BASE_URL)
    log_in(browser)
    time.sleep(WAIT_TIME_INCREMENT_IN_SEC)
    browser.get(account_info.ALL_PROBLEMS_URL)
    select_show_all_problems(browser)

    probs_and_urls = get_all_problems(browser)
    all_probs_on_site = [p[0] for p in probs_and_urls]
    # import pandas as pd
    # df = pd.DataFrame(probs_and_urls, columns=['Problem', 'URL'])
    # df.to_csv('problems.csv', index=False)

    downloaded_probs = []
    for f in [os.path.join(output_folder,f) for f in os.listdir(output_folder) if '_meta_data_' in f]:
        with open(f) as jf:
            md = json.load(jf)
            downloaded_probs.append(list(md.keys())[0])

    problems_not_downloaded = list(set(all_probs_on_site) - set(downloaded_probs))

    for prob_and_url in probs_and_urls:
        if prob_and_url[0] in problems_not_downloaded:
            meta_data = {}
            prob_name = sanitize_name(prob_and_url[0])
            prob_url = prob_and_url[1]
            browser.get(prob_url)
            time.sleep(WAIT_TIME_INCREMENT_IN_SEC) # wait 5 secs to load everything

            prob_difficulty = browser.find_element_by_xpath('//div[@data-cy="question-title"]/following-sibling::div/div[1]').text
            company_and_frequency = get_comapnies_and_asked_frequencies(browser)
            related_topics = get_related_topics(browser)
            similar_questions = get_similar_questions(browser)
            meta_data[prob_name] = {'difficulty': prob_difficulty,
                                    'companies_and_freq': company_and_frequency,
                                    'related_topics': related_topics,
                                    'similar_questions': similar_questions}
            print("\n=>Saving problem desc:", prob_name)
            print(json.dumps(meta_data[prob_name], indent=4, sort_keys=True), "\n")
            # datetime.now().strftime('%Y%m%d%H%M%S')
            save_problem_desc_screenshot(browser,
                                         os.path.join(output_folder,
                                                      ''.join([prob_difficulty, '_', prob_name, '_prob_',
                                                               datetime.now().strftime('%Y%m%d'), '.png'])))

            click_on_solution_tab(browser)
            time.sleep(WAIT_TIME_INCREMENT_IN_SEC)
            no_soln_ele = browser.find_elements_by_xpath('//*[contains(text(),"No solution for this question")]')
            if not no_soln_ele:
                # Only if we do NOT see the tooltip text that says 'No solution for this question', then we proceed to take screenshots
                print("\n=>Saving solution of problem:", prob_name)
                screenshot_cnt = 1
                take_solution_screenshot(browser, screenshot_cnt, output_folder, prob_difficulty, prob_name)

                target_pixel_row = 0
                # this is the element we can scroll on
                time.sleep(3)
                solution_window = browser.find_element_by_xpath('//div[@id="solution"]/div[2]')
                # pdb.set_trace()
                # this is the element wrapper that tells us how many pixels the solution window is tall
                try:
                    solution_window_height = browser.find_element_by_xpath('//h2[contains(text(),"Solution")]/parent::div').rect['height']
                except NoSuchElementException:
                    solution_window_height = browser.find_element_by_xpath('//h4[contains(text(),"Approach")]/parent::div').rect['height']

                while (solution_window_height - FULL_WINDOW_PIXEL_HEIGHT) > 0:
                    target_pixel_row += FULL_WINDOW_PIXEL_HEIGHT
                    solution_window_height -= FULL_WINDOW_PIXEL_HEIGHT
                    js_script = ''.join(["arguments[0].scrollTo(0, window.scrollY + ", str(target_pixel_row), ");"])
                    # Example: browser.execute_script("arguments[0].scrollTo(0, window.scrollY + 1400)", s)
                    browser.execute_script(js_script, solution_window)
                    screenshot_cnt += 1
                    time.sleep(1)
                    take_solution_screenshot(browser, screenshot_cnt, output_folder, prob_difficulty, prob_name)

            meta_data_file = os.path.join(output_folder, ''.join([prob_difficulty, '_', prob_name, '_meta_data_',
                                                                  datetime.now().strftime('%Y%m%d'), '.txt']))
            with open(meta_data_file, 'w') as outfile:
                json.dump(meta_data, outfile)
                print("\n=>Saving meta data at:", meta_data_file)

    browser.close()
    print("\nFinished puzzle program.")


if __name__ == '__main__':
    main()