import csv
import scrapy
import pickle
import time
import datetime
import os

folder_path = os.getcwd() + "/src/i2p/scraper/"
urls_file_path = folder_path + "urls.csv"
results_file_path = folder_path  + "logs/logs_public.csv"
times_results = folder_path + "logs/times_results_public.csv"

results_file_path_i2p = folder_path  + "logs/logs_i2p.csv"
times_results_i2p = folder_path + "logs/times_results_i2p.csv"

def clear_files():
    files = [results_file_path, times_results, results_file_path_i2p, times_results_i2p]
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
   
