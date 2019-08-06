"""
Author: Phyo Thiha
Last Modified: August 4, 2019
Description:
Python script to generate CSV data file, which can be used for testing, with 
specified data type and row numbers.

Usage:
>> python generate_csv.py   -t 'int_id(start,step),ascii_str(min,max),float(min,max),int(min,max)'
                            -r 5000000
                            -d '|' 
                            -o 'output.csv'
                            -c 'ID,columnA,columnB,columnC,columnD' 
                            -q 'min'
Flags:
t   -   (required) comma-separated list of data types that will be generated for each column. 
        Syntax is as follows:
        int_id(start,step)  -   sequential integer IDs. Starting number and step must be defined.
                                E.g., int_id(0,1) would generate id sequence of [0,1,2,3,....]
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
        categorical(comma-separated values) - random categorical values that are chosen from
                                              comma-separated values provided.
                                              E.g., cat(1,'dog') will return either 1 or 'dog' as data.
        Note: If input parameters for the above data types aren't given, the program will use the default
        ranges/values defined as CONSTANTs in the code. In other words, one can call this program like below:
        >> python generate_csv.py -r 50000000 -d '|' -t 'int_id(),str_ids(),float(),....'
        
r   - (optional) number of rows to be generated in the output CSV file. Default is 500K rows.
d   - (optional) delimiter to be used in the output CSV file. Default is '|'.
o   - (optional) output file name. Default would be of format '<YYYYMMDDHHMMSS_numOfRows>.csv'
c   - (optional) comma-separated list of column header names. Default would be of format 
        ['<datatype>_<column_index>', '<datatype>_<column_index>',...]. For example, 
        [int_0, str_id_1, date_3, ....]
q   - (optional) quoting option. Valid options are: 'min','all','nonnumeric','none' 
       corresponding to Python CSV library's default values defined here:
       https://docs.python.org/3/library/csv.html#csv.QUOTE_ALL
       Default is 'min' (i.e. csv.QUOTE_MINIMAL)
"""
import pdb
import argparse
import csv
from datetime import datetime
from decimal import *
import random
import re
import string
import sys
import uuid

## Constants (default values) used in data types for random data generation
ID_START = 0
ID_STEP = 1

STR_LENGTH = 10
ASCII_CHARS = ''.join([string.ascii_letters, string.digits, string.punctuation])
UTF8_CHARS = ''.join(tuple(chr(i) for i in range(32, 0x110000) if chr(i).isprintable())) # REF: https://stackoverflow.com/a/39682429

MIN_NUM = -1 * round(sys.maxsize/2) # REF: https://stackoverflow.com/a/7604981
MAX_NUM = round(sys.maxsize/2)
PRECISION = 12
SCALE = 2

START_DATE = '1970-01-01' # Unix epoch date
END_DATE = '3028-06-06' # Robot uprising year in Futurama with day and month made up by me
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

CATEGORICAL_VALUES = ['TRUE', 'FALSE']

## Constants for output CSV file
ROW_NUM = 50000
DELIMITER =  '|'
QUOTE_OPTIONS = {'min': csv.QUOTE_MINIMAL,
                 'all': csv.QUOTE_ALL,
                 'nonnumeric': csv.QUOTE_NONNUMERIC,
                 'none': csv.QUOTE_NONE}


def int_id(start=ID_START, step=ID_STEP):
    """
    Generates infinite sequence of integer IDs (starting from 'start', equally spaced apart by 'step').
    REF: http://web.archive.org/web/20190717071814/https://anandology.com/python-practice-book/iterators.html
    """
    # TODO: we can expand this to produce unique string-based IDs (like MD5 hash of a string)
    i = start
    while True:
        yield i
        i = i + step


def str_id(min=STR_LENGTH, max=STR_LENGTH):
    """
    Generates unique random string ids that are of length min <= N <= max.
    REF: http://web.archive.org/save/https://pynative.com/python-generate-random-string/
    """
    str_length = random.randint(min, max)
    return uuid.uuid4().hex[0:str_length]


def ascii_str(min=STR_LENGTH, max=STR_LENGTH):
    """
    Generates random string with ASCII characters of length min <= N <= max.
    REF: http://web.archive.org/save/https://pynative.com/python-generate-random-string/
    """
    str_length = random.randint(min, max)
    return ''.join(random.choice(ASCII_CHARS) for i in range(str_length))


def utf8_str(min=STR_LENGTH, max=STR_LENGTH):
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


def numeric(precision=PRECISION, scale=SCALE):
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


def date(start=START_DATE, end=END_DATE):
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


def datetime(start=START_DATE, end=END_DATE):
    """
    Generates random date value between start and end datetime (inclusive)
    in 'YYYY-MM-DDTHH:MM:SS' (ISO 8601) format. For example, '2018-08-04T21:02:05'
    """
    return _get_random_datetime(start, end).strftime(DATETIME_FORMAT)


def categorical(values=CATEGORICAL_VALUES):
    """
    Chooses one of the comma-separated values provided as input.
    For example, categorical(1,'dog','dino') will return one of
    the three values from 1, 'dog' and 'dino' at random.
    REF: http://web.archive.org/save/https://pynative.com/python-random-choice/
    """
    return random.choice(values)


if __name__ == '__main__':
    # 1. Process arguments passed into the program
    DESC = "This script generates CSV file based on specification. Try '-h' " \
           "to learn how to use"
    ROW_HELP = "(optional) Number of rows to be generated in the output CSV file. " \
               "Default is " +  ROW_NUM + " rows."
    DELIMITER_HELP = "(optional) Delimiter to be used in the output CSV file. Default is '|'."
    OUTPUT_FILE_HELP = "(optional) Output file name. Default would be of format " \
                       "'<YYYYMMDDHHMMSS_numOfRows>.csv'"
    QUOTING_HELP = "(optional) Define much quote would be put for columns in CSV file. " \
                   "Allowed options are: 'min', 'all', 'nonnumeric' and 'none'." \
                   "Default is 'min', which is equivalent to Python's csv.QUOTE_MINIMAL."
    COLUMN_HELP = "(optional) Define custom column headers using comma-separated list like " \
                  "'ID,columnA,columnB,columnC,columnD,...' etc. " \
                  "If not provided, program will default to column names with format" \
                  "like this: '<datatypeOfColumn>_<columnIndex>,...'. Specifically, " \
                  "the default column names will look like this: " \
                  "'int_0, str_id_1, date_3, ....'"
    DATA_TYPE_HELP = "(required) Define data types for each column using comma-separated list like " \
                    "'int_id(start,step),ascii_str(min,max),float(min,max),int(min,max)'." \
                    "The allowed data types are: 'id', 'str_id', 'ascii_str', 'utf8_str', " \
                    "'float', 'numeric', 'int', 'date', 'datetime' and 'categorical'." \
                    "Please read the comment at beginning of Python script, 'generate_csv.py', " \
                    "to understand more detail about these data types and parameters needed."

    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('-r', required=False, type=int,
                        default=ROW_NUM,
                        help=ROW_HELP)
    parser.add_argument('-d', required=False, type=str,
                        default=DELIMITER,
                        help=DELIMITER_HELP)
    parser.add_argument('-o', required=False, type=str,
                        # default=,
                        help=OUTPUT_FILE_HELP)
    parser.add_argument('-q', required=False, type=str,
                        default='min',
                        help=QUOTING_HELP)
    parser.add_argument('-c', required=False, type=str,
                        help=COLUMN_HELP)
    parser.add_argument('-t', required=True, type=str,
                        help=DATA_TYPE_HELP)
    args = parser.parse_args()

    cur_datetime = datetime.now().strftime('%Y%m%d%H%M%S')

    # 2. prepare necessary parameters before generating data for CSV file
    rows = args.r
    delimiter = args.d
    output_file = ''.join([cur_datetime,'_',rows,'.csv']) if (not args.o) else args.o
    quoting = QUOTE_OPTIONS[args.q]

    ## Test string:
    ## int_id(start,step),str_id(min,max), ascii_str( min, max),utf8_str(min,max) , float (min , max ),numeric( precision, scale ),int(min , max),date(start,end),datetime(start, end),categorical('blah','1',2, 3)
    ## r'[,\s]?(.*?\(.*?\))[,\s]?' # r',?(.*?\(.*?\)),?'
    # Note: two regex patterns above are good as well, but sometimes include extra commas
    # with each split unit, so decided to use the pattern below, which produces slightly
    # cleaner splits
    re_each_data_type = r'(.*?\(.*?\))[,\s]?'
    data_types = list(filter(None, re.split(re_each_data_type, args.t)))
    re_data_type_and_params = r'(.*?)\((.*?)\)' # https://regexr.com/4indg

    # Python regex tutorial:
    # REF: http://web.archive.org/web/20190806021129/https://www.guru99.com/python-regular-expressions-complete-tutorial.html
    pdb.set_trace()
    print("ha")
    # check if column headers names is eqv in size to that of data types
