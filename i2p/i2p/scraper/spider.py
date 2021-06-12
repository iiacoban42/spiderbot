"""Requests sites with scrapy and log http status codes"""
import csv
import os
import scrapy
import pickle
import logging
import time
import datetime
import importlib
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.exceptions import NotConfigured, IgnoreRequest
from twisted.internet.error import TCPTimedOutError, TimeoutError, DNSLookupError, ConnectionRefusedError
from selenium import webdriver

util = importlib.import_module("util")
folder_path = os.getcwd() + "/i2p/i2p/scraper/"

urls_file_path = folder_path + "urls.csv"

logs_public = folder_path  + "logs/logs_public.csv"
stats_public = folder_path + "logs/stats_public.csv"
logs_i2p = folder_path  + "logs/logs_i2p.csv"
stats_i2p = folder_path + "logs/stats_i2p.csv"


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
    link_extractor = LinkExtractor()
    def start_requests(self):
        util.clear_files()
        for url in self.start_urls:
            
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
        success_cb(response, main_url, logs_public)
        links_to_crawl = [main_url]
        for i, link in enumerate(self.link_extractor.extract_links(response)):
            if(len(links_to_crawl) >= 4):
                break

            if(remove_protocol(link.url) != remove_protocol(main_url)):
                links_to_crawl.append(link.url)
                yield scrapy.Request(link.url, callback=self.parse_http_crawled, \
                            errback=self.errback_http_crawled, \
                            cb_kwargs=dict(main_url=link.url), \
                            dont_filter=True,\
                            headers=self.headers)

        
        util.append_list_as_row(links_to_crawl, folder_path + "logs/crawled_urls_pub.csv")

    def parse_http_i2p(self, response, main_url):
        # Successful request
        success_cb(response, main_url, logs_i2p)
  
        links_to_crawl = [main_url]
        for i, link in enumerate(self.link_extractor.extract_links(response)):
            if(len(links_to_crawl) >= 4):
                break
                
            if(remove_protocol(link.url) != remove_protocol(main_url)):
                links_to_crawl.append(link.url)
                yield scrapy.Request(link.url, callback=self.parse_http_crawled_i2p, \
                            errback=self.errback_http_crawled_i2p, \
                            cb_kwargs=dict(main_url=link.url), \
                            dont_filter=True, \
                            headers=self.headers, \
                            meta={
                            "proxy": "http://127.0.0.1:4444"
                                })
            
        util.append_list_as_row(links_to_crawl, folder_path + "logs/crawled_urls_i2p.csv")

    def parse_http_crawled(self, response, main_url):
        # Successful request
        log_file = folder_path + "logs/subdomains_pub.csv"
        success_cb(response, main_url, log_file)
    
    def parse_http_crawled_i2p(self, response, main_url):
        # Successful request
        log_file = folder_path + "logs/subdomains_i2p.csv"
        success_cb(response, main_url, log_file)
    
    def errback_http(self, failure, main_url=None):
        self.logger.error(repr(failure))
        err_cb(failure, logs_public)
        

    def errback_http_i2p(self, failure, main_url=None):
        self.logger.error(repr(failure))
        err_cb(failure, logs_i2p)

    def errback_http_crawled(self, failure, main_url=None):
        self.logger.error(repr(failure))
        log_file = folder_path + "logs/subdomains_pub.csv"
        err_cb(failure, log_file)


    def errback_http_crawled_i2p(self, failure, main_url=None):
        self.logger.error(repr(failure))
        log_file = folder_path + "logs/subdomains_i2p.csv"
        err_cb(failure, log_file)

    def close(self, reason):
        start_time = self.crawler.stats.get_value('start_time')
        finish_time = self.crawler.stats.get_value('finish_time')

        util.compile_stats(logs_public, stats_public, start_time, finish_time)
        util.compile_stats(logs_i2p, stats_i2p, start_time, finish_time)

def err_cb(failure, log_file):
    end_time = datetime.datetime.now().timestamp()  
    request = failure.request

    if failure.check(IgnoreRequest("Forbidden by robots.txt")):
        util.append_list_as_row(["robots.txt", end_time, request.url], log_file)
    #if isinstance(failure.value, HttpError):
    elif failure.check(HttpError):
        response = failure.value.response
        if 'captcha' in response.meta.keys():
            util.append_list_as_row(["CAPTCHA", end_time, request.url], log_file)
        else:
            util.append_list_as_row([response.status, end_time, request.url], log_file)

    #elif isinstance(failure.value, DNSLookupError):
    elif failure.check(DNSLookupError):
        request = failure.request
        util.append_list_as_row(["DNSLookupError", end_time, request.url], log_file)

    #elif isinstance(failure.value, TCPTimedOutError):
    elif failure.check(TCPTimedOutError):
        request = failure.request
        util.append_list_as_row(["TCPTimeout", end_time, request.url], log_file)

    #elif isinstance(failure.value, TimeoutError):
    elif failure.check(TimeoutError):
        request = failure.request
        util.append_list_as_row(["TimeoutError", end_time, request.url], log_file)
    else:
        util.append_list_as_row(["Err", end_time, request.url], log_file)

def success_cb(response, main_url, log_file):
    end_time = datetime.datetime.now().timestamp()

    if 'captcha' in response.meta.keys():
        util.append_list_as_row(["CAPTCHA", end_time, main_url, response.url], log_file)
    else:
        util.append_list_as_row([response.status, end_time, main_url, response.url], log_file)

def remove_protocol(url):
    if url.startswith('http'):
        url = re.sub(r'^https?:\/\/', '', url)
    if url.startswith('www.'):
        url = re.sub(r'www.', '', url)
    return url.strip('/')
