# Ads.txt Checker by Jamie K

"""
Use case: Extract Ads.txt document from website

Usage:
Use command prompt to run python and this script, with the input file (required) next to this module's name

>>> python AdsTxtCheck.py <filename.xlsx>

"""

import multiprocessing as mp
import requests
import numpy as np
import pandas as pd
import re
import sys
import time
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine


def standard_input(url):
    """Standardize beginning of URL"""
    if url.startswith('http://'):
        return url

    elif url.startswith('www.'):
        rx = str('http://' + url)
        return rx

    else:
        rz = str('http://www.' + url)
        return rz


def standard_input_end(url_2):
    """Standardize end of URL"""
    url_3 = str(url_2 + '/ads.txt')
    return url_3


def no_ads_txt(url, url_2, resp):
    """Function to handle all cases of non-ads.txt compliant sites"""
    non_ads_out_dict = dict()
    non_ads_out_dict['flag'] = "No ads.txt"
    non_ads_out_dict['domain'] = url
    non_ads_out_dict['ads_txt_url'] = url_2
    non_ads_out_dict['exchange_name'] = "No ads.txt"
    non_ads_out_dict['exchange_id'] = "No ads.txt"
    non_ads_out_dict['seller_type'] = "No ads.txt"
    non_ads_out_dict['datetime_refreshed'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    non_ads_out_dict['comments'] = resp

    return non_ads_out_dict


def adtxtcrawl(sites):
    """Ads.txt parser. Args: sites - an iterable containing the domains to scrape, q - py's multiprocessing Queue function"""
    func_dict_list = []  # Declare list of dictionaries to append data
    for url in sites:
        url = url.replace(" ", "").lower()
        transform_url = standard_input(url)
        transform_url_2 = standard_input_end(transform_url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36 - Mindshare Media Agency NYC <jamiec.khoo@mindshareworld.com>'}
        print('Working On: ' + transform_url_2)
        try:  # Try-except block to handle HTML connection errors
            r = requests.get(transform_url_2, headers=headers, timeout=60, allow_redirects=True)
            if r.status_code == requests.codes.ok and "error 404" in r.text.lower():
                func_dict_list.append(no_ads_txt(url, transform_url_2, resp="HTTP 200 but received error in HTML body"))

            elif r.status_code == requests.codes.ok and "error 404" not in r.text.lower():
                for i in r.text.split('\n'):
                    inside_list = []
                    inside_list.append(i)
                    out_dict = dict()

                    for it in inside_list:
                        try:
                            out_dict['flag'] = "With ads.txt"
                            out_dict['domain'] = url
                            out_dict['ads_txt_url'] = transform_url_2
                            out_dict['exchange_name'] = it.split(',')[0]
                            out_dict['exchange_id'] = it.split(',')[1]
                            out_dict['seller_type'] = it.split(',')[2].split('#')[0].lower().strip()
                            out_dict['datetime_refreshed'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                            out_dict['comments'] = it.split('#')[1]

                        except IndexError:
                            pass

                    import pdb
                    pdb.set_trace()
                    func_dict_list.append(out_dict)

            else:  # Block to handle non 200 HTTP response
                func_dict_list.append(no_ads_txt(url, transform_url_2, resp=r.status_code))

        except requests.exceptions.RequestException as e:  # Block to handle HTML connection error
            print('URL: {} ERROR MESSAGE: {}'.format(transform_url_2, str(e)))
            func_dict_list.append(no_ads_txt(url, transform_url_2, resp=str(e)[:100]))

        except Exception as e:  # Block to handle general errors (not related to connection)
            print('URL: {} ERROR MESSAGE: {}'.format(transform_url_2, str(e)))
            func_dict_list.append(no_ads_txt(url, transform_url_2, resp=str(e)[:100]))


if __name__ == '__main__':
    start_time = time.time()
    sites = [
            'http://www.espn.com/ads.txt',
        ]
    adtxtcrawl(sites)