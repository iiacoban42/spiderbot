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

n = 300
start_from = 200
start_urls = util.get_top_websites(n, start_from)
PROXY = "127.0.0.1:4444"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

def run_spider():
    i = start_from
    for url in start_urls:
        with webdriver.Chrome(options=chrome_options) as i2p_driver:
            try:
                save = screenshot_i2p + str(i) +'i2p.png'
                i2p_driver.get(url)
                time.sleep(2)
                i2p_driver.save_screenshot(save)
            
            except TimeoutException:
                print('i2p timeout on ' + str(i))
        
        with webdriver.Chrome() as driver:
            try:
                save = screenshot_pub + str(i) +'pub.png'
                driver.get(url)
                time.sleep(2)
                driver.save_screenshot(save)
        
            except TimeoutException:
                print('pub timeout on ' + str(i))
        
        i += 1
        

        

run_spider()