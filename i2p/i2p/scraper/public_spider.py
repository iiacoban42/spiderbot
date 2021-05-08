import csv
import os
import scrapy
import pickle
import logging
import time
import datetime
import importlib

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


class SpiderBot(scrapy.Spider):
    name = "spiderbot"
    n = 500
    start_urls = util.get_top_websites(n)
    end_times = []
    def start_requests(self):
        util.clear_files()
        for url in self.start_urls:
            
            # yield SeleniumRequest(url=url, callback=self.parse_http, errback=self.errback_http, dont_filter=True)

            yield scrapy.Request(url, callback=self.parse_http,
                                    errback=self.errback_http,
                                    dont_filter=True)

    def parse_http(self, response):
        # Successful request
        end_time = datetime.datetime.now().timestamp()
        self.end_times.append(end_time)

        self.logger.error('Got successful response from {}'.format(response.url))
        util.append_list_as_row([response.status, end_time,  response.url], results_file_path)


    def errback_http(self, failure):
        # log all errback failures
        self.logger.error(repr(failure))
        end_time = datetime.datetime.now().timestamp()
        self.end_times.append(end_time)

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            response = failure.value.response
            util.append_list_as_row([response.status, end_time, response.url], results_file_path)
            self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            request = failure.request
            util.append_list_as_row(["DNSLookupError", end_time, request.url], results_file_path)
            self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TCPTimedOutError):
        elif failure.check(TCPTimedOutError):
            request = failure.request
            util.append_list_as_row(["TCPTimeout", end_time, request.url], results_file_path)
            self.logger.error('TCPTimeout on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            util.append_list_as_row(["TimeoutError", end_time, request.url], results_file_path)
            self.logger.error('TimeoutError on %s', request.url)

    def close(self, reason):
        start_time = self.crawler.stats.get_value('start_time').timestamp()
        finish_time = self.crawler.stats.get_value('finish_time').timestamp()
        util.compile_stats(results_file_path, stats, finish_time-start_time)