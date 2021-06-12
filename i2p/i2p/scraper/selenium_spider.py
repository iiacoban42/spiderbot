import csv
import os
import pickle
import logging
import time
import datetime
import importlib
import time
import re
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
# screenshot_pub = folder_path + "screenshots/pub/"
# screenshot_i2p = folder_path + "screenshots/i2p/"

screenshot_pub = folder_path + "screenshots/experiment/"
screenshot_i2p = folder_path + "screenshots/experiment/"

def success(site):
    if (re.search("^2..", site) or re.search("^3..", site)):
        return True
    return False   


def get_sites(n, start_from=0):
    # Parse urls.csv file
    urls = []
    folder_path = os.getcwd() + "/i2p/i2p/scraper/"
    urls_file_path = folder_path + "experiment.csv"
    # urls_file_path = folder_path + "crawled_urls.csv"
    with open(urls_file_path) as csv_file:
        reader = csv.reader(csv_file)
        for i, line in enumerate(reader):
            if i>=n:
                return urls
            if i>=start_from:
                domains = []
                for j in range(len(line)):
                    domains.append(line[j])
                urls.append(domains)

        return urls

n = 500
start_from = 0
# start_urls = util.get_top_websites(n, start_from)
start_urls = get_sites(n, start_from)
PROXY = "127.0.0.1:4444"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
# chrome_options.add_extension(folder_path+"extentions/ad-block.crx")
chrome_options.add_extension(folder_path+"extentions/cookie.crx")


chrome_options_pub = webdriver.ChromeOptions()
# chrome_options_pub.add_extension(folder_path+"extentions/ad-block.crx")
chrome_options_pub.add_extension(folder_path+"extentions/cookie.crx")

def run_spider():
    main_domain = start_from

    for url in start_urls:
        sub_domain = 0
        for link in url:
            
            image = screenshot_i2p + str(main_domain)+"_"+ str(sub_domain)+'i2p.png'

            if(os.path.exists(image)):
                sub_domain +=1
                continue

            with webdriver.Chrome(options=chrome_options) as i2p_driver:
                try:
                    save = screenshot_i2p + str(main_domain)+"_"+ str(sub_domain)+'i2p.png'
                    i2p_driver.get(link)
                    time.sleep(1)
                    i2p_driver.save_screenshot(save)
                
                except TimeoutException:
                    print('i2p timeout on ' + str(main_domain)+"_"+ str(sub_domain))
                    continue

            with webdriver.Chrome(options=chrome_options_pub) as driver:
                try:
                    save = screenshot_pub + str(main_domain)+"_"+ str(sub_domain) +'pub.png'
                    driver.get(link)
                    time.sleep(1)
                    driver.save_screenshot(save)
        
                except TimeoutException:
                    print('pub timeout on ' + str(main_domain)+"_"+ str(sub_domain))

            sub_domain += 1
        
        main_domain += 1


run_spider()
