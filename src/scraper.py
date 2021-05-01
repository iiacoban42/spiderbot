import csv
import os
import scrapy
import pickle

urls_file_path = os.getcwd() + "/src/urls.csv"
results_file_path = os.getcwd() + "/src/logs.csv"

def get_top_websites(n):
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
    def parse(self, response):
        append_list_as_row([response.status, response.url])
