#!/usr/bin/env python
import matplotlib.pyplot as plt
import csv
import pickle
import time
import datetime
import os
import re
from collections import Counter
path = os.getcwd() + '/i2p/i2p/scraper/diff_stats/stats/'
path_i2p = os.getcwd() + '/i2p/i2p/scraper/diff_stats/stats/code_stats_i2p.csv'
path_public = os.getcwd() + '/i2p/i2p/scraper/diff_stats/stats/code_stats_public.csv'
# The slices will be ordered and plotted counter-clockwise.

def create_pie_chart(labels, sizes, name):
    # labels = [r'Rayos X (88.4 %)', r'RMN en solucion (10.6 %)', 
    # r'Microscopia electronica (0.7 %)', r'Otros (0.3 %)']
    # sizes = [88.4, 10.6, 0.7, 0.3]
    # colors = ['orange', 'gold', 'lightskyblue']
    patches, texts = plt.pie(sizes, startangle=90)
    plt.legend(patches, labels, loc="best")
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.tight_layout()
    # plt.figtext(0.5, 0.01, caption, wrap=True, horizontalalignment='center', fontsize=12)
    plt.savefig(name + '.png')
    plt.show()

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

total_samples = 1520
blocked = round(27 /total_samples * 100, 2)
partly_blocked = round(126 /total_samples *100, 2)
not_blocked = round(1367 / total_samples * 100, 2)
create_pie_chart(["Not Blocked " + str(not_blocked) + "%",\
                    "Blocked " + str(blocked) + "%", \
                    "Partly Blocked " + str(partly_blocked) + "%"],\
                    [not_blocked, blocked, partly_blocked],  "blocking")

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

