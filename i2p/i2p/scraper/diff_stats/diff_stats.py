import csv
import pickle
import time
import datetime
import os
import re
from collections import Counter
path = os.getcwd() + '/i2p/i2p/scraper/diff_stats/stats/'
path_public = os.getcwd() + '/i2p/i2p/scraper/diff_stats/stats/logs_public.csv'
path_i2p = os.getcwd() + '/i2p/i2p/scraper/diff_stats/stats/logs_i2p.csv'

def write_to_file(file, arr):
    with open(file, "w") as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerows(arr)

def status_codes_stats(responce_codes, stats_file):
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

def success(site):
    if (re.search("^2..", site) or re.search("^3..", site)):
        return True
    return False

def dup(a):
    seen = {}
    dupes = []

    for x in a:
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.append(x)
            seen[x] += 1
    return dupes

def remove_protocol(url):
    if url.startswith('http'):
        url = re.sub(r'https?:\\', '', url)
    if url.startswith('www.'):
        url = re.sub(r'www.', '', url)
    return url

def get_diff_stats():
    responce_i2p = []
    responce_public = []
    websites_i2p = []
    websites_public = []
    with open(path_public) as csv_file:
        reader = csv.reader(csv_file)
        for i, line in enumerate(reader):
            responce_public.append(line[0])
            websites_public.append(line[2])

    with open(path_i2p) as csv_file:
        reader = csv.reader(csv_file)
        for i, line in enumerate(reader):
            responce_i2p.append(line[0])
            websites_i2p.append(line[2])

    for url in websites_i2p:
        url = remove_protocol(url)
    for url in websites_public:
        url = remove_protocol(url)

    rejected_i2p = []
    rejected_public = []
    rejected_both = []
    accepted_both = []

    status_codes_i2p = []
    status_codes_public = []
    misc = []

    for i, i2p_site in enumerate(websites_i2p):
        for j, pub_site in enumerate(websites_public):
            if i2p_site == pub_site:
                status_codes_i2p.append(responce_i2p[i])
                status_codes_public.append(responce_public[j])

                if success(responce_i2p[i]) and success(responce_public[j]):
                    accepted_both.append([responce_public[j], responce_i2p[i], i2p_site])

                elif success(responce_i2p[i]):
                    rejected_public.append([responce_public[j], responce_i2p[i], i2p_site])

                elif success(responce_public[j]):
                    rejected_i2p.append([responce_public[j], responce_i2p[i], i2p_site])

                else: rejected_both.append([responce_public[j], responce_i2p[i], i2p_site])

    union = []
    union.extend(accepted_both)
    union.extend(rejected_both)
    union.extend(rejected_i2p)
    union.extend(rejected_public)

    i2p_misc = set(websites_i2p)
    pup_misc = set(websites_public)

    print(dup(websites_i2p))

    write_to_file(path + "accepted_both.csv", accepted_both)
    write_to_file(path + "rejected_both.csv", rejected_both)
    write_to_file(path + "rejected_i2p.csv", rejected_i2p)
    write_to_file(path + "rejected_public.csv",  rejected_public)

    status_codes_stats(status_codes_i2p, path + "code_stats_i2p.csv")
    status_codes_stats(status_codes_public, path + "code_stats_public.csv")

    total = len(rejected_i2p) + len(rejected_public) + len(rejected_both) + len(accepted_both) 
    p_rejected_i2p = len(rejected_i2p)  / total * 100
    p_rejected_public = len(rejected_public)  / total * 100
    p_rejected_both = len(rejected_both)  / total * 100
    p_accepted_both = len(accepted_both)  / total * 100
    print('rejected i2p: ' + str(len(rejected_i2p)) + " out of "+ str(total)+" -> " + str(p_rejected_i2p)+"%")
    print('rejected public: ' + str(len(rejected_public)) + " out of "+ str(total)+" -> " + str(p_rejected_public)+"%")
    print('rejected both: ' + str(len(rejected_both)) + " out of "+ str(total)+" -> " + str(p_rejected_both)+"%")
    print('accepted both: ' + str(len(accepted_both)) + " out of "+ str(total)+" -> " + str(p_accepted_both)+"%")

    print(len(i2p_misc))
    print(len(pup_misc))

get_diff_stats()




