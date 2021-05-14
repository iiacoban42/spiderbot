import csv
import os
import scrapy
import pickle
import logging
import time
import datetime
import importlib
import time
from scrapy_splash import SplashRequest
from Screenshot import Screenshot_Clipping
from webdriver_manager.chrome import ChromeDriverManager

from scrapy.spidermiddlewares.httperror import HttpError
from scrapy_selenium import SeleniumRequest
from twisted.internet.error import TCPTimedOutError, TimeoutError, DNSLookupError
from selenium import webdriver

util = importlib.import_module("util")
folder_path = os.getcwd() + "/i2p/i2p/scraper/"

urls_file_path = folder_path + "urls.csv"
results_file_path = folder_path  + "logs/logs_public.csv"
times_results = folder_path + "logs/times_results_public.csv"
stats = folder_path + "logs/stats_public.csv"
save_screenshot = folder_path + "screenshots/pup/"

class SpiderBot(scrapy.Spider):
    name = "spiderbot"
    n = 1
    # start_urls = util.get_top_websites(n)
    star_urls = ['facebook.com']
    end_times = []
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    headers =  {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }
    
    # def start_requests(self):
    #     util.clear_files()
    #     for url in self.start_urls:
            
    #         yield SeleniumRequest(url=url, callback=self.parse_http, errback=self.errback_http, dont_filter=True)


    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def parse(self, response):
        # Successful request
        end_time = datetime.datetime.now().timestamp()
        self.end_times.append(end_time)
        self.driver.get(response)
        ob=Screenshot_Clipping.Screenshot()
        ob.full_Screenshot(self.driver, save_path=save_screenshot, image_name='Myimage.png')
        util.append_list_as_row([response.status, end_time,  response.url], results_file_path)

    def errback_http(self, failure):
        # log all errback failures
        self.logger.error(repr(failure))
        end_time = datetime.datetime.now().timestamp()
        # self.end_times.append(end_time)

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            response = failure.value.response
            util.append_list_as_row([response.status, end_time, response.url], results_file_path)
            # self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            request = failure.request
            util.append_list_as_row(["DNSLookupError", end_time, request.url], results_file_path)
            # self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TCPTimedOutError):
        elif failure.check(TCPTimedOutError):
            request = failure.request
            util.append_list_as_row(["TCPTimeout", end_time, request.url], results_file_path)
            # self.logger.error('TCPTimeout on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            util.append_list_as_row(["TimeoutError", end_time, request.url], results_file_path)
            # self.logger.error('TimeoutError on %s', request.url)

    def close(self, reason):
        start_time = self.crawler.stats.get_value('start_time').timestamp()
        finish_time = self.crawler.stats.get_value('finish_time').timestamp()
        util.compile_stats(results_file_path, stats, finish_time-start_time)
        self.driver.close()

        self.driver.quit()

