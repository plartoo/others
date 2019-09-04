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

import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import account_info

# Note: define the location of folder where Chrome driver saves downloaded files
DOWNLOAD_FOLDER = 'C:\\Users\\phyo.thiha\\Downloads'
BASE_URL = 'https://national-tv.rentrak.com'
# Assumes that "chromedrive/chromedriver.exe" shares same PARENT folder as this script
parent_folder = os.path.dirname(os.path.normpath(os.getcwd()))
chromedriver_exe_with_path = os.path.join(parent_folder , 'chromedriver', 'chromedriver.exe')
print("\nInvoking Chrome driver at:", chromedriver_exe_with_path, "\n")
browser = webdriver.Chrome(executable_path=chromedriver_exe_with_path)

browser.get(BASE_URL)
browser.find_element_by_id('login_id').clear()
browser.find_element_by_id('password').clear()
browser.find_element_by_id('login_id').send_keys(account_info.USERNAME)
browser.find_element_by_id('password').send_keys(account_info.PASSWORD)
browser.find_element_by_css_selector('input[type=\"submit\"]').click()

# market_monthly_trend_menu = browser.find_elements_by_xpath("//a[contains(text(),'Market Monthly Trend')]")[0]
# market_monthly_url = market_monthly_trend_menu.get_attribute('href')
# # We can also wait before clicking on the market_monthly_trend_menu above
# # REF: https://stackoverflow.com/questions/56119289/element-not-interactable-selenium
# browser.get(market_monthly_url)

cur_datetime = datetime.now()
# We have decided to fetch YTD data (January of current year) to (current month of current year)
from_date = ''.join([cur_datetime.strftime('%Y'),'0101'])
to_date = ''.join([cur_datetime.strftime('%Y%m'),'01'])

# We will use the following primary bookmarks to fetch different months and networks
# DoNotDelete_Automation_Market_Monthly_Trend_All_Networks_All_Markets
# DoNotDelete_Automation_Network_Monthly_Trend_A-L_Networks_All_Markets
# DoNotDelete_Automation_Network_Monthly_Trend_M-Z_Networks_All_Markets
bookmarks = ["'DoNotDelete_Automation_Network_Monthly_Trend_A-L_Networks_All_Markets'",]
for b in bookmarks:
    print("Processing bookmark:", b)
    bookmark_ele = browser.find_elements_by_xpath("//a[contains(text(),{0})]".format(b))[0]
    bookmark_url = bookmark_ele.get_attribute('href')
    print("Extracted bookmark URL:", bookmark_url)
    browser.get(bookmark_url)

    browser.find_element_by_xpath('//*[@id="simple_month_range_from_select"]/option[contains(text(), "{0}")]'.format(from_date)).click()
    browser.find_element_by_xpath('//*[@id="simple_month_range_to_select"]/option[contains(text(), "{0}")]'.format(to_date)).click()
    pdb.set_trace()


    #
    # excel_download_ele = browser.find_elements_by_xpath("//*[@title='Download Report to Excel']")[0]
    # excel_download_url = excel_download_ele.get_attribute('href')
    # print("Downloading excel file from URL:", excel_download_url)
    # browser.get(excel_download_url)
    # # We will infer latest downloaded file name from getctime
    # # REF: https://stackoverflow.com/q/17958987
    # downloaded_file_name = max([os.path.join(DOWNLOAD_FOLDER, f) for f in os.listdir(DOWNLOAD_FOLDER)],
    #                            key=os.path.getctime)
    # print("\nDownloaded file named:", downloaded_file_name)


# A
# https://national-tv.rentrak.com/reports/monthly_network_trend_analysis.html?simple_month_range=20150101+00%3A00%3A00&simple_month_range=20151201+00%3A00%3A00&network_no=3_4_6_438_441_8779_5095_6459_341_342_6116_625_328_32_7540_330_629_553_372_345_367_375_379_674_482_11257_11539_8913_371_9850_397_319_8040_24_5063_366_5985_5203_9894_8842_12278_7635_1_7645_331_326_332_395_401_2073_8006_40_8082_8808_676_396_8036_413_5069_558_675_475_489_634_635_7726_-38354_637_550_478_278_415_8072_8092_31_354_623_355_28_671_627_36_2077_381_8096_1310_565_2210_8151_673_406_29_559_462_455_19_667_666_5968_297_12_572_551_562_580_556_552_387_622_495_480_12274_431_5729_12276_471_289_321_1260_11691_27_630_6261_385_472_5289_6018_2086_7667_7740_8090_2072_2076_140_33_639_640_641_642_650_568_567_5396_8068_8070_324_409_296_311_286_386_7242&tv_market_no=&go=Loading...&apply_ranker__hidden=false&dvr_bucket=within_72_hours&is_service_network_ready=1&dsr_sort_TrendViewsByNetworkMonth=network_long_name_and_name+broadcast_month&dsr_hideshow_hh_rating=hh_rating&dsr_hideshow_live=live

MONTHLY_MARKET_TREND_URL = '/reports/market_month_trend.html'

print('Done')





