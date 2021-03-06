"""Create pie chart stats"""
import matplotlib.pyplot as plt
import csv
import pickle
import time
import datetime
import os
import re
from collections import Counter
from statsmodels.stats.proportion import proportions_ztest
path = os.getcwd() + '/i2p/i2p/scraper/diff_stats/stats/'
path_i2p = os.getcwd() + '/i2p/i2p/scraper/diff_stats/stats/code_stats_i2p.csv'
path_public = os.getcwd() + '/i2p/i2p/scraper/diff_stats/stats/code_stats_public.csv'

def create_pie_chart(labels, sizes, name):
    patches, texts = plt.pie(sizes, startangle=90)
    plt.legend(patches, labels, loc="lower center")
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(name + '.png')
    plt.show()

def generate_status_codes_pie():
    i2p_codes = []
    i2p_percent = []
    pub_codes = []
    pub_percent = []

    with open(path_public) as csv_file:
        reader = csv.reader(csv_file)
        for i, line in enumerate(reader):
            percent = str(round(float(line[2]), 2)) + "%"
            pub_codes.append(line[0] + " " + percent)
            pub_percent.append(line[2])


    with open(path_i2p) as csv_file:
        reader = csv.reader(csv_file)
        for i, line in enumerate(reader):
            percent = str(round(float(line[2]), 2)) + "%"
            i2p_codes.append(line[0] + " " + percent)
            i2p_percent.append(line[2])

    create_pie_chart(i2p_codes, i2p_percent,  "i2p_pie")
    create_pie_chart(pub_codes, pub_percent,  "pub_pie")

def generate_blocking_proportions():
    total_samples = 1520
    blocked = round(27 /total_samples * 100, 2)
    partly_blocked = round(126 /total_samples *100, 2)
    not_blocked = round(1367 / total_samples * 100, 2)
    create_pie_chart(["Not Blocked " + str(not_blocked) + "%",\
                        "Blocked " + str(blocked) + "%", \
                        "Partly Blocked " + str(partly_blocked) + "%"],\
                        [not_blocked, blocked, partly_blocked],  "blocking")

def generate_blocked_content_pie():
    total_samples = 126
    missing_img = round(55 /total_samples * 100, 2)
    missing_scripts = round(12 /total_samples *100, 2)
    missing_info = round(6 / total_samples * 100, 2)
    missing_interract = round(34 / total_samples * 100, 2)
    missing_img_and_interract = round(19 / total_samples * 100, 2)

    val = [
    missing_img,
    missing_interract,
    missing_img_and_interract,
    missing_scripts,
    missing_info,
    ]

    lables = [
    "Images " + str(missing_img) + "%",
    "Interractive elements " + str(missing_interract) + "%",
    "Images and interractive elements " + str(missing_img_and_interract) + "%",
    "Scripts " + str(missing_scripts) + "%",
    "Other information " + str(missing_info) + "%"
    ]

    create_pie_chart(lables, val,  "partial-blocking")

def generate_categorized_blocking_websites_pie():
    urls_file_path = "i2p/i2p/scraper/classified.csv"
    lables = []
    with open(urls_file_path) as csv_file:
        reader = csv.reader(csv_file)
        for i, line in enumerate(reader):
            lables.append(line[1])

    freq = dict(Counter(lables))
    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    values = []
    lables = []
    n = sum(freq.values())
    for key, val in freq.items():
        p = round(val / n * 100, 2)
        lables.append(key + " " + str(p) + "%")
        values.append(p)
    create_pie_chart(lables, values,  "categories")

def generate_pie_charts():
    generate_blocking_proportions()
    generate_status_codes_pie()
    generate_blocked_content_pie()
    generate_categorized_blocking_websites_pie()


def test_hypothesis_proportions():
    # source: https://sonalake.com/latest/hypothesis-testing-of-proportion-based-samples/
    # can we assume anything from our sample
    significance = 0.05
    # our sample - 89% are good
    sample_success = 1367
    sample_size = 1520

    # our Ho is  85%
    null_hypothesis = 0.85
    # check our sample against Ho for Ha > Ho
    # for Ha < Ho use alternative='smaller'
    # for Ha != Ho use alternative='two-sided'
    stat, p_value = proportions_ztest(count=sample_success, nobs=sample_size, value=null_hypothesis, alternative='larger')
    # report
    print('z_stat: %0.3f, p_value: %0.3f' % (stat, p_value))
    if p_value > significance:
        print ("Fail to reject the null hypothesis - we have nothing else to say")
    else:
        print ("Reject the null hypothesis - suggest the alternative hypothesis is true")

generate_pie_charts()
#z_stat: 6.394, p_value: 0.000
#Reject the null hypothesis - suggest the alternative hypothesis is true
test_hypothesis_proportions()