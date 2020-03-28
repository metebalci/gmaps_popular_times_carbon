#!/usr/bin/env python3

'''
Run the google maps popularity scraper
'''

import os
import sys
import time
import urllib.parse
import traceback
import socket
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# load local params from config.py
import config

# generate unique runtime for this job
run_time = datetime.now().strftime('%Y%m%d_%H%M%S')

def main():
    urls = pd.read_csv('urls.csv')

    url_list = urls.iloc[:, 0].tolist()
    url_name_list = urls.iloc[:, 1].tolist()
    for (url, url_name) in zip(url_list, url_name_list):
        print('processing: ' + url)
        print('processing: ' + url_name)

        carbon_ts = int(time.time())

        try:
            data = run_scraper(url, url_name)
        except:
            traceback.print_last()
            print('ERROR:', url, run_time)
            # go to next url
            continue

        if data is not None:
            print(data)

            sock = socket.socket()
            sock.connect((config.CARBON_SERVER, int(config.CARBON_PORT)))
            for (data_name, data_value) in data:
                message = 'popular_times.%s.%s %f %d\n' % (url_name, data_name, data_value, carbon_ts)
                sock.sendall(message.encode('ascii'))
            sock.close()

            print('DONE:', url, run_time)

        else:
            print('WARNING: no data', url, run_time)


def run_scraper(url, url_name):
    # because scraping takes some time, write the actual timestamp instead of the runtime
    scrape_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # get html source (note this uses headless Chrome via Selenium)
    html = get_html(url, 'html' + os.sep + url_name + '.' + run_time + '.html')
    if html is None:
        return None

    # parse html (uses beautifulsoup4)
    data = parse_html(html)

    return data


def get_html(u,file_name):

    # if the html source exists as a local file, don't bother to scrape it
    # this shouldn't run
    if False and os.path.isfile(file_name):
        with open(file_name,'r') as f:
            html = f.read()
        return html
    else:
        # requires chromedriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        # https://stackoverflow.com/a/55152213/2327328
        # I choose German because the time is 24h, less to parse
        options.add_argument('--lang=de-DE')
        options.binary_location = config.CHROME_BINARY_LOCATION
        chrome_driver_binary = config.CHROMEDRIVER_BINARY_LOCATION
        d = webdriver.Chrome(chrome_driver_binary, options=options)

        # get page
        d.get(u)

        # sleep to let the page render, it can take some time
        try:
            WebDriverWait(d, config.SLEEP_SEC).until(EC.presence_of_element_located((By.CLASS_NAME, 'section-popular-times-bar')))
        except TimeoutException:
            print('ERROR: Timeout waiting for the section popular times')
            return None

        # save html local file
        if config.SAVE_HTML:
            with open(file_name, 'w') as f:
                f.write(d.page_source)

        # save html as variable
        html = d.page_source

        d.quit()
        return html


def parse_html(html):
    soup = BeautifulSoup(html,features='html.parser')
    pops = soup.find_all('div', {'class': 'section-popular-times-bar'})
    hour = 0
    dow = 0
    data = []

    print('len(pops): %d' % len(pops))

    for pop in pops:
        # note that data is stored sunday first, regardless of the local
        t = pop['aria-label']

        # in german page, aria-label is one of these:
        # print(t)
        # for current hour: Derzeit zu 11 % ausgelastet; normal sind 68 %.
        # for all other hours: Um 13 Uhr zu 60 % ausgelastet.

        hour_prev = hour
        freq_now = None

        try:
            # need to check all cases because normal case does not mention the hour
            if 'normal' not in t:
                hour = int(t.split()[1]) # part at index 1 is hour, see above
                freq = int(t.split()[4]) # part at index 4 is average percent
            else:
                # the current hour has special text
                # hour is the previous value + 1
                hour = hour + 1
                freq = int(t.split()[-2]) # part at last-2 index is average percent
                freq_now = int(t.split()[2]) # part at index 2 is the current percent

                return [('average', freq), ('current', freq_now), ('ratio', (100*freq_now)/freq)]

            if hour < hour_prev:
                # increment the day if the hour decreases
                dow += 1

        except:
            # if a day is missing, the line(s) won't be parsable
            # this can happen if the place is closed on that day
            # skip them, hope it's only 1 day per line,
            # and increment the day counter
            dow += 1

    return None

if __name__ == '__main__':
    main()
