import os

from selenium import webdriver

CHROME_DRIVER_FOLDER_NAME = 'chromedriver'
path_to_chromedriver = os.path.join(os.path.dirname(os.path.normpath(os.getcwd())), CHROME_DRIVER_FOLDER_NAME)

browser = webdriver.Chrome(executable_path = path_to_chromedriver)

