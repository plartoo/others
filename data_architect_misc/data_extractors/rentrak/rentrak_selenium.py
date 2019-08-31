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

from selenium import webdriver


BASE_URL = 'https://national-tv.rentrak.com'
# assumes that chromedriver exe file is in the same root folder as this script
CHROME_DRIVER_FOLDER_NAME = 'chromedriver'
path_to_chromedriver = os.path.join(os.path.dirname(os.path.normpath(os.getcwd())), CHROME_DRIVER_FOLDER_NAME)

browser = webdriver.Chrome(executable_path = path_to_chromedriver)

