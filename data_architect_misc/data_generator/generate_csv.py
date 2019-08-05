import pdb
"""
Author: Phyo Thiha
Last Modified: August 4, 2019
Description:
Python script to generate CSV data file, which can be used for testing, with 
specified data type and row numbers.

Usage:
>> python generate_csv.py   -r 5000000 
                            -d '|' 
                            -t 'id(start,step),ascii_str(min,max),float(min,max,precision),int(min,max)'
                            -o 'output.csv' 
                            -c 'ID,columnA,columnB,columnC,columnD' 
                            -q 'min'
Flags:
r   - (required) number of rows to be generated in the output CSV file
d   - (required) delimiter to be used in the output CSV file
t   - (required) data types that will be generated for each column. Syntax is as follows:
        id(start,step)      -   sequential integer IDs. Starting number and step must be defined.
                                E.g., id(0,1) would generate id sequence of [0,1,2,3,....]
        str_id(min,max)     -   universally unique random string IDs of length between min and max.
                                E.g., 'Ef735p#2O]'
        ascii_str(min,max)  -   string with random ASCII characters of length between min and max length.
                                E.g., ascii_str(3,4) would generate str sequence of ['ABC','AZDE','QDS',...]
        utf8_str(min,max)   -   same as 'ascii_str' above, but generates UTF-8 characters.
        float(min,max)      -   random float numbers between min and max.
        numeric(precision, scale)   -   random decimal number with total number of digits equal to 
                                        'precision' and decimals equalling 'scale'.
                                        E.g., numeric(10,2) will yield something like '12345678.90'
        int(min,max)                -   random integer numbers between min and max.
        date(start,end)             -   random date between start and end in STRING format.
                                        E.g., date('2018-01-01','2018-12-31') would generate random dates
                                        between Jan 1, 2018 and Dec 31, 2018 (both inclusive) 
                                        in ISO 8601-compliant format ('YYYY-MM-DD').
        datetime(start,end)         -   random date time between start and end in STRING format. 
                                        Similar to 'date(start,end)', datetime(2018-01-01','2018-12-31') 
                                        would generate random date and time between 
                                        Jan 1, 2018 and Dec 31, 2018 (both inclusive)
                                        in this ISO 8601-compliant format ('YYYY-MM-DDTHH:MM:SS').
                                        E.g., date('2018-01-01','2018-12-31') might yield
                                        '2018-08-04T21:03:23'.
        categorical([values])       -   random categorical values that are chosen from the list of values provided.
                                        E.g., cat[1,'dog'] will return either 1 or 'dog' as data.
        Note: If input parameters for the above data types aren't given, the program will use the default
        ranges/values defined as CONSTANTs in the code. In other words, one can call this program like below:
        >> python generate_csv.py -r 50000000 -d '|' -t 'id(),str_ids(),float(),....' 
        
o   - (optional) output file name. Default would be of format '<YYYYMMDDHHMMSS_numOfRows>.csv'
c   - (optional) column header names. Default would be of format ['Column_A', 'Column_B',...]
q   - (optional) quoting option. Valid options are: 'min','all','nonnumeric','none' 
       corresponding to Python CSV library's default values defined here:
       https://docs.python.org/3/library/csv.html#csv.QUOTE_ALL
       Default is 'min' (i.e. csv.QUOTE_MINIMAL)
"""

import argparse
import csv
from datetime import datetime
from decimal import *
import os
import random
import string
import sys
import uuid


ID_START = 0
ID_STEP = 1
STR_DEFAULT_LENGTH = 10
ASCII_CHARS = ''.join([string.ascii_letters, string.digits, string.punctuation])
# REF: https://stackoverflow.com/q/1477294 and https://stackoverflow.com/a/39682429
UTF8_CHARS = ''.join(tuple(chr(i) for i in range(32, 0x110000) if chr(i).isprintable()))
DEFAULT_PRECISION = 2
MIN_NUM = -1 * round(sys.maxsize/2) # REF: REF: https://stackoverflow.com/a/7604981
MAX_NUM = round(sys.maxsize/2)
DEFAULT_PRECISION = 12
DEFAULT_SCALE = 2
DEFAULT_START_DATE = '1970-01-01' # Unix epoch date
DEFAULT_END_DATE = '3028-06-06' # Robot uprising year in Futurama with day and month made up by me
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
DEFAULT_CATEGORICAL_VALUES = ['TRUE','FALSE']


def id(start=ID_START, step=ID_STEP):
    """
    Generates infinite sequence of integer IDs (starting from 'start', equally spaced apart by 'step').
    REF: http://web.archive.org/web/20190717071814/https://anandology.com/python-practice-book/iterators.html
    """
    # TODO: we can expand this to produce unique string-based IDs (like MD5 hash of a string)
    i = start
    while True:
        yield i
        i = i + step


def str_id(min=STR_DEFAULT_LENGTH, max=STR_DEFAULT_LENGTH):
    """
    Generates unique random string ids that are of length min <= N <= max.
    REF: http://web.archive.org/save/https://pynative.com/python-generate-random-string/
    """
    str_length = random.randint(min, max)
    return uuid.uuid4().hex[0:str_length]


def ascii_str(min=STR_DEFAULT_LENGTH, max=STR_DEFAULT_LENGTH):
    """
    Generates random string with ASCII characters of length min <= N <= max.
    REF: http://web.archive.org/save/https://pynative.com/python-generate-random-string/
    """
    str_length = random.randint(min, max)
    return ''.join(random.choice(ASCII_CHARS) for i in range(str_length))


def utf8_str(min=STR_DEFAULT_LENGTH, max=STR_DEFAULT_LENGTH):
    """
    Generates random utf-8 printable characters of length min <= N <= max.
    """
    str_length = random.randint(min, max)
    return ''.join(random.choice(UTF8_CHARS) for i in range(str_length))


def float(min=MIN_NUM, max=MAX_NUM):
    """
    Generates random float number between min and max (min <= N <= max).
    REF: http://web.archive.org/web/20190804005156/https://pynative.com/python-get-random-float-numbers/
    """
    return random.uniform(min, max)


def numeric(precision=DEFAULT_PRECISION, scale=DEFAULT_SCALE):
    """
    Generates random decimal numbers with total digits equalling 'precision'
    and decimal scale equalling 'scale'.
    E.g., numeric(11,4) would yield '8211753.5117'
    """
    getcontext().prec = precision
    exponent = (precision - scale)
    return Decimal(10**exponent) * Decimal(random.random())


def int(min=MIN_NUM, max=MAX_NUM):
    """
    Generates random integer between min and max (min <= N <= max).
    REF: https://stackoverflow.com/a/7604981
    Note: Here, default value for max is whatever the host OS allows.
    Having max as sys.maxsize might decrease the performance,
    so we should consider reducing it later.
    """
    return random.randint(min, max)


def _get_random_int_between(n1, n2):
    return random.randint(min(n1, n2), max(n1, n2))


def _get_random_date(start, end):
    """Helper function that returns datetime object with date value."""
    start_date = datetime.strptime(start, DATE_FORMAT)
    end_date = datetime.strptime(end, DATE_FORMAT)
    y = _get_random_int_between(start_date.year, end_date.year)
    m = _get_random_int_between(start_date.month, end_date.month)
    d = _get_random_int_between(start_date.day, end_date.day)
    return datetime(y, m, d)


def date(start=DEFAULT_START_DATE, end=DEFAULT_END_DATE):
    """
    Generates random date value between start and end date (inclusive)
    in 'YYYY-MM-DD' (ISO 8601) format. For example, '2018-08-04'
    """
    return _get_random_date(start, end).strftime(DATE_FORMAT)


def _get_random_datetime(start, end):
    """Helper function that returns datetime object with both date and time values."""
    date = _get_random_date(start, end)
    h = _get_random_int_between(0, 24)
    m = _get_random_int_between(0, 60)
    s = _get_random_int_between(0, 60)
    return datetime(date.year, date.month, date.day, h, m, s)


def datetime(start=DEFAULT_START_DATE, end=DEFAULT_END_DATE):
    """
    Generates random date value between start and end datetime (inclusive)
    in 'YYYY-MM-DDTHH:MM:SS' (ISO 8601) format. For example, '2018-08-04T21:02:05'
    """
    return _get_random_datetime(start, end).strftime(DATETIME_FORMAT)


def categorical(list_of_values=DEFAULT_CATEGORICAL_VALUES):
    """
    Chooses one of the values provided in the list at random.
    REF: http://web.archive.org/save/https://pynative.com/python-random-choice/
    """
    return random.choice(list_of_values)


if __name__ == '__main__':
    # 1. Process arguments passed into the program
    parser = argparse.ArgumentParser(description="This script generates CSV file based on specification. Try '-h' to "
                                                 "learn how to use")

    # python generate_csv.py -s 5000000 (required)
    #                       -d '|'
    #                       -o 'output.csv' (optional. Default: timestamp_rowcount.csv)
    #                       -t 'id(start,step),str(min,max),float(x,y,precision),int(min,max),date(start,end),datetime(start,end),categorical([values])'
    #                       -c 'col1,col2,col3,col4,col5,...' (optional)
    #                       -q 'min/all/nonnumeric/none' (quote optional)
    #
    #
    parser.add_argument('-c', required=True, type=str,
                        help='TODO') # TODO: write help message here
    args = parser.parse_args()

    # 2. Load JSON configuration file
    if (not args.c) or (not os.path.exists(args.c)):
        sys.exit('TODO') # TODO: write proper error message here