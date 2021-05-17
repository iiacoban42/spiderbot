import csv
import os
import scrapy
import pickle
import logging
import time
import datetime
import importlib

from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.exceptions import NotConfigured, IgnoreRequest
from twisted.internet.error import TCPTimedOutError, TimeoutError, DNSLookupError
from selenium import webdriver

util = importlib.import_module("util")
folder_path = os.getcwd() + "/i2p/i2p/scraper/"

urls_file_path = folder_path + "urls.csv"

logs_public = folder_path  + "logs/logs_public.csv"
stats_public = folder_path + "logs/stats_public.csv"
logs_i2p = folder_path  + "logs/logs_i2p.csv"
stats_i2p = folder_path + "logs/stats_i2p.csv"
# times_results = folder_path + "logs/times_results_public.csv"


class SpiderBot(scrapy.Spider):
    name = "spiderbot"
    n = 500
    start_urls = util.get_top_websites(n)
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
    def start_requests(self):
        util.clear_files()
        for url in self.start_urls:
            
            # yield SeleniumRequest(url=url, callback=self.parse_http, errback=self.errback_http, dont_filter=True)
            # public request
            yield scrapy.Request(url, callback=self.parse_http, \
                                    errback=self.errback_http, \
                                    cb_kwargs=dict(main_url=url), \
                                    dont_filter=True,\
                                    headers=self.headers)
            # i2p request
            yield scrapy.Request(url, callback=self.parse_http_i2p, \
                                    errback=self.errback_http_i2p, \
                                    cb_kwargs=dict(main_url=url), \
                                    dont_filter=True, \
                                    headers=self.headers, \
                                    meta={
                                    "proxy": "http://127.0.0.1:4444"
                                        })
    
    def parse_http(self, response, main_url):
        # Successful request
        end_time = datetime.datetime.now().timestamp()
        self.end_times.append(end_time)

        if 'captcha' in response.meta.keys():
            util.append_list_as_row(["CAPTCHA", end_time, main_url, response.url], logs_public)
        else:
        # self.logger.error('Got successful response from {}'.format(response.url))
            util.append_list_as_row([response.status, end_time, main_url, response.url], logs_public)

    def parse_http_i2p(self, response, main_url):
        # Successful request
        end_time = datetime.datetime.now().timestamp()
        self.end_times.append(end_time)
        
        if 'captcha' in response.meta.keys():
            util.append_list_as_row(["CAPTCHA", end_time, main_url, response.url], logs_i2p)
        # self.logger.error('Got successful response from {}'.format(response.url))
        else:
            util.append_list_as_row([response.status, end_time, main_url, response.url], logs_i2p)


    def errback_http(self, failure, main_url=None):
        # log all errback failures
        request = failure.request
        self.logger.error(repr(failure))
        end_time = datetime.datetime.now().timestamp()
        self.end_times.append(end_time)
        
        if failure.check(IgnoreRequest("Forbidden by robots.txt")):
            util.append_list_as_row(["robots.txt", end_time, request.url], logs_public)
        #if isinstance(failure.value, HttpError):
        elif failure.check(HttpError):
            response = failure.value.response

            if 'captcha' in response.meta.keys():
                util.append_list_as_row(["CAPTCHA", end_time, request.url], logs_public)
            else:
                util.append_list_as_row([response.status, end_time, request.url], logs_public)
            # self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            util.append_list_as_row(["DNSLookupError", end_time, request.url], logs_public)
            # self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TCPTimedOutError):
        elif failure.check(TCPTimedOutError):
            util.append_list_as_row(["TCPTimeout", end_time, request.url], logs_public)
            # self.logger.error('TCPTimeout on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            util.append_list_as_row(["TimeoutError", end_time, request.url], logs_public)
            # self.logger.error('TimeoutError on %s', request.url)
        else:
            util.append_list_as_row(["Err", end_time, request.url], logs_public)

    def errback_http_i2p(self, failure, main_url=None):
        # log all errback failures
        request = failure.request

        self.logger.error(repr(failure))
        end_time = datetime.datetime.now().timestamp()
        self.end_times.append(end_time)
        
        if failure.check(IgnoreRequest("Forbidden by robots.txt")):
            util.append_list_as_row(["robots.txt", end_time, request.url], logs_i2p)
        #if isinstance(failure.value, HttpError):
        elif failure.check(HttpError):
            response = failure.value.response
            if 'captcha' in response.meta.keys():
                util.append_list_as_row(["CAPTCHA", end_time, request.url], logs_i2p)
            else:
                util.append_list_as_row([response.status, end_time, request.url], logs_i2p)
            # self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            util.append_list_as_row(["DNSLookupError", end_time, request.url], logs_i2p)
            # self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TCPTimedOutError):
        elif failure.check(TCPTimedOutError):
            util.append_list_as_row(["TCPTimeout", end_time, request.url], logs_i2p)
            # self.logger.error('TCPTimeout on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            util.append_list_as_row(["TimeoutError", end_time, request.url], logs_i2p)
            # self.logger.error('TimeoutError on %s', request.url)
        else:
            util.append_list_as_row(["Err", end_time, request.url], logs_i2p)

    def close(self, reason):
        start_time = self.crawler.stats.get_value('start_time')
        finish_time = self.crawler.stats.get_value('finish_time')
        print(start_time)
        print(finish_time)
        start_time = start_time.timestamp()
        finish_time = finish_time.timestamp()
        util.compile_stats(logs_public, stats_public, finish_time-start_time)
        util.compile_stats(logs_i2p, stats_i2p, finish_time-start_time)
