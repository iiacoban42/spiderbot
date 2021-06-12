"""Identify which sites blocked i2p"""
import os
import shutil
import importlib
import csv
util = importlib.import_module("util")
folder_path = os.getcwd() + "/i2p/i2p/scraper/"
screenshot_partly_blocked = folder_path + "screenshots/partly_blocked/"
screenshot_blocked = folder_path + "screenshots/blocked/"

def get_sites(n, start_from=0):
    # Parse urls.csv file
    urls = []
    folder_path = os.getcwd() + "/i2p/i2p/scraper/"
    # urls_file_path = folder_path + "experiment.csv"
    urls_file_path = folder_path + "crawled_urls.csv"
    with open(urls_file_path) as csv_file:
        reader = csv.reader(csv_file)
        for i, line in enumerate(reader):
            if i>=n:
                return urls
            if i>=start_from:
                domains = []
                for j in range(len(line)):
                    domains.append(line[j])
                urls.append(domains)

        return urls

def get_blocking_websites():
    blocking_websites = []

    for file_name in os.listdir(screenshot_partly_blocked):
        if "i2p" not in file_name:
            continue

        site_index = file_name.split('_')
        subdomain = site_index[1].split('i')
        blocking_websites.append((int(site_index[0]), int(subdomain[0])))

    for file_name in os.listdir(screenshot_blocked):
        if "i2p" not in file_name:
            continue
        site_index = file_name.split('_')
        subdomain = site_index[1].split('i')
        blocking_websites.append((int(site_index[0]), int(subdomain[0])))

    return blocking_websites

dataset = get_sites(500)
blocking_websites = get_blocking_websites()

for t in blocking_websites:
    blocking_website = dataset[t[0]][t[1]]
    util.append_list_as_row([blocking_website], "i2p/i2p/scraper/blocking_websites.csv")