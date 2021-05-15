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
screenshot = folder_path + "screenshots/pup/"

n = 1
start_urls = util.get_top_websites(n)

def run_spider():

    driver = webdriver.Chrome()

    for url in start_urls:

        driver.get(url)
        
        
        save = screenshot + 'test' +'.png'
        driver.save_screenshot(save)
        
        time.sleep(2)
    
    driver.close()

run_spider()