import csv
import pickle
import time
import datetime
import os
from collections import Counter

folder_path = os.getcwd() + "/i2p/i2p/scraper/"
# urls_file_path = folder_path + "urls.csv"
urls_file_path = folder_path + "top500Domains.csv"
results_file_path = folder_path  + "logs/logs_public.csv"
subdom_pub = folder_path + "logs/subdomains_pub.csv"

results_file_path_i2p = folder_path  + "logs/logs_i2p.csv"
subdom_i2p = folder_path + "logs/subdomains_i2p.csv"
stats_public = folder_path + "logs/stats_public.csv"
stats_i2p = folder_path + "logs/stats_i2p.csv"

crawled_links = folder_path + "logs/crawled_urls_pub.csv"
crawled_links_i2p = folder_path + "logs/crawled_urls_i2p.csv"
def clear_files():
    files = [results_file_path, subdom_pub, results_file_path_i2p, subdom_i2p,\
         stats_i2p, stats_public, crawled_links, crawled_links_i2p]
    for file in files:
        open(file, 'w').close()

def get_top_websites(n, start_from=0):
    # Parse urls.csv file
    urls = []
    with open(urls_file_path) as csv_file:
        reader = csv.reader(csv_file)
        for i, line in enumerate(reader):
            if i>=n:
                return urls
            if i>=start_from:
                urls.append('http://' + line[1])

        return urls

def append_list_as_row(list_of_elem, file):
    # Open file in append mode
    with open(file, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
   
def compile_stats(logs_file, stats_file, start, end):
    responce_codes = []
    with open(logs_file) as csv_file:
        reader = csv.reader(csv_file)
        for i, line in enumerate(reader):
            responce_codes.append(line[0])

    n = len(responce_codes)
    freq = dict(Counter(responce_codes))

    res = []
    for key in freq:
        frequency = freq[key]
        freq_percent = freq[key] / n * 100 
        res.append([key, frequency, str(freq_percent) + "%"])
   
    with open(stats_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(res)

    append_list_as_row(['started', start], stats_file)
    append_list_as_row(['ended', end], stats_file)
    
