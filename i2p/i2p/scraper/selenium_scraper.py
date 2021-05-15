import csv
import os
import pickle
import logging
import time
import datetime
import importlib
import time
import urllib as url
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

util = importlib.import_module("util")
folder_path = os.getcwd() + "/i2p/i2p/scraper/"

urls_file_path = folder_path + "urls.csv"
results_file_path = folder_path  + "logs/logs_public.csv"
times_results = folder_path + "logs/times_results_public.csv"
stats = folder_path + "logs/stats_public.csv"
screenshot_pub = folder_path + "screenshots/pub/"
screenshot_i2p = folder_path + "screenshots/i2p/"

n = 1
start_urls = util.get_top_websites(n)
PROXY = "127.0.0.1:4444"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

def run_spider():

    for url in start_urls:
        with webdriver.Chrome(chrome_options=chrome_options) as i2p_driver:
            save = screenshot_i2p + 'test' +'.png'
            i2p_driver.get(url)
            time.sleep(2)
            i2p_driver.save_screenshot(save)
        
        
        with webdriver.Chrome() as driver:
            save = screenshot_pub + 'test' +'.png'
            driver.get(url)
            time.sleep(2)
            driver.save_screenshot(save)
        

run_spider()