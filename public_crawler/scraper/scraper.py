import csv
import os
import scrapy
import pickle
import logging
import time
import datetime
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TCPTimedOutError, TimeoutError, DNSLookupError

urls_file_path = os.getcwd() + "/public_crawler/scraper/urls.csv"
results_file_path = os.getcwd() + "/public_crawler/scraper/logs.csv"
times_results = os.getcwd() + "/public_crawler/scraper/times_results.csv"

def clear_files():
    files = [results_file_path, times_results]
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
   


class SpiderBot(scrapy.Spider):
    name = "spiderbot"
    n = 10
    start_urls = get_top_websites(n)
    end_times = []
    def start_requests(self):
        clear_files()
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_http,
                                    errback=self.errback_http,
                                    dont_filter=True)

    def parse_http(self, response):
        # Successful request
        end_time = datetime.datetime.now().timestamp()
        self.end_times.append(end_time)

        self.logger.error('Got successful response from {}'.format(response.url))
        append_list_as_row([response.status, end_time,  response.url], results_file_path)


    def errback_http(self, failure):
        # log all errback failures
        self.logger.error(repr(failure))
        end_time = datetime.datetime.now().timestamp()
        self.end_times.append(end_time)

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            response = failure.value.response
            append_list_as_row([response.status, end_time, response.url], results_file_path)
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
        start_time = self.crawler.stats.get_value('start_time').timestamp()
        
        elapsed = []
        end_times_copy = self.end_times.copy()
        elapsed.append([end_times_copy[0] - start_time])
        for i in range(1, self.n):
            time_diff = end_times_copy[i] - self.end_times[i-1] 
            elapsed.append([time_diff])

        with open(times_results, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(elapsed)
