import csv
import os
import scrapy
import pickle
import logging
import time
import datetime
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TCPTimedOutError, TimeoutError, DNSLookupError

urls_file_path = os.getcwd() + "/src/urls.csv"
results_file_path = os.getcwd() + "/src/logs.csv"
times = os.getcwd() + "/src/times.csv"
times_results = os.getcwd() + "/src/times_results.csv"

def clear_files():
    files = [results_file_path, times, times_results]
    for file in files:
        open(file, 'w').close()

def get_top_websites(n):
    # Parse urls.csv file
    urls = []
    with open(urls_file_path) as csv_file:
        reader = csv.reader(csv_file)
        for i, line in enumerate(reader):
            if i>=n:
                return urls
            urls.append('http://' + line[1])

        return urls

def append_list_as_row(list_of_elem, file):
    # Open file in append mode
    with open(file, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def get_time_stats(start):
    elapsed = []
    with open(times) as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            time_diff = float(line[0]) - float(start)
            elapsed.append([time_diff])
    
    with open(times_results, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(elapsed)

class SpiderBot(scrapy.Spider):
    name = "spiderbot"
    start_urls = get_top_websites(10)
    def start_requests(self):
        clear_files()
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_http,
                                    errback=self.errback_http,
                                    dont_filter=True)

    def parse_http(self, response):
        # Successful request
        append_list_as_row([datetime.datetime.now().timestamp()], times)
        self.logger.error('Got successful response from {}'.format(response.url))
        append_list_as_row([response.status, response.url], results_file_path)


    def errback_http(self, failure):
        # log all errback failures
        self.logger.error(repr(failure))
        append_list_as_row([datetime.datetime.now().timestamp()], times)

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            response = failure.value.response
            append_list_as_row([response.status, response.url], results_file_path)
            self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            request = failure.request
            append_list_as_row(["DNSLookupError", request.url], results_file_path)
            self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TCPTimedOutError):
        elif failure.check(TCPTimedOutError):
            request = failure.request
            append_list_as_row(["TCPTimeout", request.url], results_file_path)
            self.logger.error('TCPTimeout on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            append_list_as_row(["TimeoutError", request.url], results_file_path)
            self.logger.error('TimeoutError on %s', request.url)

    def close(self, reason):
        start_time = self.crawler.stats.get_value('start_time')
        get_time_stats(start_time.timestamp())

