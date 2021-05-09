import csv
import pickle
import time
import datetime
import os
from collections import Counter
path = os.getcwd() + '/i2p/i2p/scraper/cumulative_stats/stats/'

def get_cumulative_stats():
    responce_ok = []
    websites = []
    for file in os.listdir(path):
        with open(path + file) as csv_file:
            reader = csv.reader(csv_file)
            for i, line in enumerate(reader):
                websites.append(line[1])
                if line[0] == '200':
                    responce_ok.append(line[1])
    # remove duplicates                
    websites = list(dict.fromkeys(websites))
    responce_ok = list(dict.fromkeys(responce_ok))
    total = len(websites)
    total_ok = len(responce_ok)
    percent = total_ok / total * 100
    print('websites with responce 200 :' + str(total_ok) + " out of "+ \
         str(total)+" -> " + str(percent)+"%")

get_cumulative_stats()



