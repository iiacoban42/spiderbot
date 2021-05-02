import csv
import os
import scrapy
import pickle
import logging
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TCPTimedOutError, TimeoutError, DNSLookupError

urls_file_path = os.getcwd() + "/src/urls.csv"
results_file_path = os.getcwd() + "/src/logs.csv"

def get_top_websites(n):
    # Parse urls.csv file
    urls = []
    with  open(urls_file_path) as csv_file:
        reader = csv.reader(csv_file)
        for i, line in enumerate(reader):
            if i>=n:
                return urls
            urls.append('http://' + line[1])

        return urls

def append_list_as_row(list_of_elem):
    # Open file in append mode
    with open(results_file_path, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

class SpiderBot(scrapy.Spider):
    name = "spiderbot"
    start_urls = get_top_websites(500)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_http,
                                    errback=self.errback_http,
                                    dont_filter=True)

    def parse_http(self, response):
        # Successful request
        self.logger.error('Got successful response from {}'.format(response.url))
        append_list_as_row([response.status, response.url])


    def errback_http(self, failure):
        # log all errback failures
        self.logger.error(repr(failure))

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            response = failure.value.response
            append_list_as_row([response.status, response.url])
            self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            request = failure.request
            append_list_as_row(["DNSLookupError", request.url])
            self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TCPTimedOutError):
        elif failure.check(TCPTimedOutError):
            request = failure.request
            append_list_as_row(["TCPTimeout", request.url])
            self.logger.error('TCPTimeout on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            append_list_as_row(["TimeoutError", request.url])
            self.logger.error('TimeoutError on %s', request.url)

