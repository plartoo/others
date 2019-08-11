"""
Author: Phyo Thiha
Last Modified: August 10, 2019
Description:
Python script to generate CSV data file, which can be used for testing, with 
specified data type and row numbers.

Usage:
>> python generate_csv.py   -t 'int_id(1,1),ascii_str(8,15),double(0.5,3.0),integer(-10,10)'
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
        double(min,max)     -   random float (aka double) numbers between min and max.
        numeric(precision, scale)   -   random decimal number with total number of digits equal to 
                                        'precision' and decimals equalling 'scale'.
                                        E.g., numeric(10,2) will yield something like '12345678.90'
        integer(min,max)            -   random integer numbers between min and max.
        date(start,end)             -   random date between start and end in STRING format.
                                        E.g., date('2018-01-01','2018-12-31') would generate random dates
                                        between Jan 1, 2018 and Dec 31, 2018 (both inclusive) 
                                        in ISO 8601-compliant format ('YYYY-MM-DD').
        date_time(start,end)        -   random date time between start and end in STRING format.
                                        Similar to 'date(start,end)', date_time(2018-01-01','2018-12-31')
                                        would generate random date and time between 
                                        Jan 1, 2018 and Dec 31, 2018 (both inclusive)
                                        in this ISO 8601-compliant format ('YYYY-MM-DDTHH:MM:SS').
                                        E.g., date_time('2018-01-01','2018-12-31') might yield
                                        '2018-08-04T21:03:23'.
        categorical(comma-separated values) - random categorical values that are chosen from
                                              comma-separated values provided.
                                              E.g., categorical(1,'dog',"dino") will return
                                              either 1 or 'dog' as data.
        Note: If input parameters for the above data types aren't given, the program will use the default
        ranges/values defined as CONSTANTs in the code. In other words, one can call this program like below:
        >> python generate_csv.py -r 50000000 -d '|' -t 'int_id(),str_ids(),double(),....'
        
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
v   - (optional) If set to '1', the program will print more info to stdout about
       what it is doing. If set to '0', the program will print only essential
       information.
"""
import argparse
import csv
from datetime import datetime
from decimal import *
from functools import partial
import random
import re
import string
import sys
import types
import uuid

## Global variable to set verbosity of stdout
verbose = 1

## Constants (default values) used to generate random data
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

## Other constants such as row number in CSV output file, quoting level, etc.
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


def double(min=MIN_NUM, max=MAX_NUM):
    """
    Generates random float (double) number between min and max (min <= N <= max).
    REF: http://web.archive.org/web/20190804005156/https://pynative.com/python-get-random-float-numbers/
    Note: We can go as high as max value in 'sys.float_info', but decided to keep this
    smaller to align with integer's min and max value.
    """
    return random.uniform(min, max)


def numeric(precision=PRECISION, scale=SCALE):
    """
    Generates random decimal numbers with total digits equaling 'precision'
    and decimal scale equaling 'scale'.
    E.g., numeric(11,4) would yield '8211753.5117'
    """
    getcontext().prec = precision
    exponent = (precision - scale)
    return Decimal(10**exponent) * Decimal(random.random())


def integer(min=MIN_NUM, max=MAX_NUM):
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
    h = _get_random_int_between(0, 23)
    m = _get_random_int_between(0, 59)
    s = _get_random_int_between(0, 59)
    return datetime(date.year, date.month, date.day, h, m, s)


def date_time(start=START_DATE, end=END_DATE):
    """
    Generates random date and time value between start and end (inclusive)
    in 'YYYY-MM-DDTHH:MM:SS' (ISO 8601) format. For example, '2018-08-04T21:02:05'
    """
    return _get_random_datetime(start, end).strftime(DATETIME_FORMAT)


def categorical(values=CATEGORICAL_VALUES):
    """
    Chooses one of the comma-separated values provided as input.
    For example, categorical(1,'dog',"dino") will return one of
    the three values from 1, 'dog' and 'dino' at random.
    REF: http://web.archive.org/save/https://pynative.com/python-random-choice/
    """
    return random.choice(values)


def _parse_data_type_definitions(input_str):
    """
    Parse comma-separated data type string (input) into a list of
    individual data type definitions (removing empty strings).
    E.g., For test string,
    "int_id(5,2),str_id(8,10), ascii_str( 8, 12),utf8_str(8,12) ,
    double (1.5 , 5.6 ), numeric ( 10, 4 ),integer(-5 , 5000),
    date('2018-01-01','2019-12-12'),date_time('2018-01-01','2019-12-12'),
    categorical('blah','1',2, 3)"
    this function returns ['int_id(start,step)', 'str_id(min,max)',' ascii_str( min, max)',....].
    See https://regexr.com/4indg for live example.

    Note: r'[,\s]?(.*?\(.*?\))[,\s]?' # r',?(.*?\(.*?\)),?'
    Two regex patterns above are good as well, but sometimes include extra commas
    with each split unit, so decided to use the pattern below, which produces slightly
    cleaner splits.
    """
    return list(filter(None, re.split(r'(.*?\(.*?\))[,\s]?', input_str)))


def _get_data_type_name_and_parameter(input_str):
    """Splits individual data type definition with parameters into
    data type name and parameters. For example, for input string
    ' , double (min , max )', this function returns the tuple
    ('double', 'min , max ').
    """
    return re.findall(r'(.*?)\((.*?)\)', input_str)


def _remove_non_word_chars(input_str):
    """Removes space character, commas, etc."""
    return re.sub(r'\W*?', '', input_str)


def _get_parameters(param_str):
    """Split parameters, if any, in a string into a list."""
    if not param_str.strip():
        # if empty string like 'int_id()' as input
        return []
    else:
        return [i.strip() for i in param_str.split(',')]


def _starts_with_quotes(s):
    # returns true if string starts with single or double quotes
    return not (not re.match(r'^[\'"]', s, re.M))


def _ends_with_quotes(s):
    # returns true if string ends with single or double quotes
    return not (not re.match(r'.*[\'"]$', s, re.M))


def _remove_start_and_end_quotes(s):
    return re.sub(r'[\'"]$', '', re.sub(r'^[\'"]', '', s))


def _parse_mixed_params(params):
    """Parse mixed list of params including str's, ints and floats"""
    processed = []
    for p in [i.strip() for i in params]:
        if _starts_with_quotes(p) and _ends_with_quotes(p):
            # if in quotes, assume the value is of str type
            processed.append(_remove_start_and_end_quotes(p))
        else:
            # if not in quotes, it could be either decimal or int
            try:
                processed.append(int(p))
            except ValueError:
                try:
                    processed.append(float(p))
                except ValueError:
                    processed.append(p)
            except:
                sys.exit("ERROR: parsing mixed param =>",
                         p, " has caused error.")
    return processed


def _parse_date_and_date_time_params(params):
    processed = []
    for t in [i.strip() for i in params]:
        if _starts_with_quotes(t) and _ends_with_quotes(t):
            # if in quotes, assume the value is of str type
            processed.append(_remove_start_and_end_quotes(t))
        else:
            processed.append(t)
    return processed


def _parse_double_params(params):
    return [float(i.strip()) for i in params]


def _parse_integer_params(params):
    return [int(i.strip()) for i in params]


def _make_partial(funcs, data_type, params):
    """
    Build and return partial function out of the data_type string
    and associated parameters. These partial functions will be called
    when we generate CSV rows.
    """
    if not params:
        # if no parameters were provided, go with defaults
        return partial(funcs[data_type])

    if data_type == 'categorical':
        p = _parse_mixed_params(params)
        v_print("\n=> Data type:", data_type, "\tParsed params:", p, "\n")
        # in categorical case, we return immediately because its params are different
        return partial(funcs[data_type], p)
    elif data_type in ['date_time', 'date']:
        p = _parse_mixed_params(params)
    elif data_type == 'double':
        p = _parse_double_params(params)
    elif data_type == 'int_id':
        p = _parse_integer_params(params)
        # in int_id case, we return a generator function instead of a partial
        return funcs[data_type](p[0], p[1])
    elif data_type in ['str_id', 'ascii_str', 'utf8_str', 'numeric', 'integer']:
        p = _parse_integer_params(params)
    else:
        sys.exit("ERROR: data type '", data_type, "' is not supported.")

    v_print("\n=> Data type:", data_type, "\tParsed params:", str(p))
    return partial(funcs[data_type], p[0], p[1])


def v_print(*a, **k):
    """
    Extend python's print function to allow for verbose argument.
    REF: https://stackoverflow.com/a/5980173
    """
    if verbose:
        print(*a, **k)
    else:
        lambda *a, **k: None


def main():
    # constants for descriptions and instructions
    DESC = "This script generates CSV file based on specification. Try '-h' " \
           "to learn the usage."
    ROW_HELP = ''.join(["(optional) Number of rows to be generated "
                        "in the output CSV file. Default is ",
                        str(ROW_NUM) , " rows."])
    DELIMITER_HELP = "(optional) Delimiter to be used in the output CSV file. Default is '|'."
    OUTPUT_FILE_HELP = "(optional) Output file name. Default would be of format " \
                       "'<YYYYMMDDHHMMSS_numOfRows>.csv'"
    QUOTING_HELP = "(optional) Define how much quote would be wraped around each " \
                   "cell in CSV file. Allowed options are: 'min', 'all', 'nonnumeric' " \
                   "and 'none'. Default is 'min', which is equivalent to Python's " \
                   "csv.QUOTE_MINIMAL."
    COLUMN_HELP = "(optional) Define custom column headers using comma-separated " \
                  "list like 'ID,columnA,columnB,columnC,columnD,...' etc. " \
                  "If not provided, program will default to column names with format" \
                  "like this: '<datatypeOfColumn>_<columnIndex>,...'. Specifically, " \
                  "the default column names will look like this: " \
                  "'int_0, str_id_1, date_3, ....'"
    VERBOSE_HELP = "(optional) If set to '1', the program will print more info to stdout" \
                   "about what it is doing. If set to '0', the program will print only " \
                   "essential information."
    DATA_TYPE_HELP = "(required) Define data types for each column using comma-separated " \
                     "list like 'int_id(start,step),ascii_str(min,max),double(min,max)," \
                     "integer(min,max)'. The allowed data types are: 'id', 'str_id', " \
                     "'ascii_str', 'utf8_str', 'double', 'numeric', 'int', 'date', " \
                     "'date_time' and 'categorical'. Please read the comment at the " \
                     "beginning of Python script, 'generate_csv.py', to understand " \
                     "more detail about these data types and parameters needed."

    # random data generator functions for different data types
    FUNCS = {
            'categorical': categorical,
            'date_time': date_time,
            'date': date,
            'double': double,
            'int_id': int_id,
            'str_id': str_id,
            'ascii_str': ascii_str,
            'utf8_str': utf8_str,
            'numeric': numeric,
            'integer': integer
        }

    # 1. acquire command line arguments
    global verbose
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('-r', required=False, type=int,
                        default=ROW_NUM,
                        help=ROW_HELP)
    parser.add_argument('-d', required=False, type=str,
                        default=DELIMITER,
                        help=DELIMITER_HELP)
    parser.add_argument('-o', required=False, type=str,
                        help=OUTPUT_FILE_HELP)
    parser.add_argument('-q', required=False, type=str,
                        default='min',
                        help=QUOTING_HELP)
    parser.add_argument('-c', required=False, type=str,
                        help=COLUMN_HELP)
    parser.add_argument('-v', required=False, type=int,
                        default=verbose,
                        help=VERBOSE_HELP)
    parser.add_argument('-t', required=True, type=str,
                        help=DATA_TYPE_HELP)
    args = parser.parse_args()

    # 2. prepare necessary parameters to generate data for CSV file
    rows = args.r
    delimiter = args.d
    quoting = QUOTE_OPTIONS[args.q]
    verbose = args.v
    cur_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
    output_file = ''.join([cur_datetime,'_',str(rows),'.csv']) if (not args.o) else args.o

    # 3. parse input string from user and start creating def's for data generation
    generator_funcs = []
    default_column_names = []
    i = 1
    for s in _parse_data_type_definitions(args.t):
        for dp in _get_data_type_name_and_parameter(s):
            data_type = _remove_non_word_chars(dp[0])
            try:
                params = _get_parameters(dp[1])
            except:
                sys.exit("ERROR: Parising this input data type=>", s,
                         ". Try 'python generate_csv.py -h' "
                         "to learn the correct usage.")

            # 4. create partial functions to generate random data for each column
            generator_funcs.append(_make_partial(FUNCS, data_type, params))
            # 5. create default column names in case user doesn't provide them
            param_str = '_'.join([p.strip("'").strip('"') for p in params])
            default_column_names.append('_'.join([data_type, param_str, str(i)]))
            i += 1

    # 6. now check and see if user provided column names of his/her choice
    if not args.c:
        col_names = default_column_names
    else:
        user_provided_col_names = args.c.split(',')
        if len(user_provided_col_names) != len(generator_funcs):
            sys.exit("ERROR: if you provide custom column names, you must "
                     "provide enough of these names to cover all data columns")
        else:
            col_names = user_provided_col_names

    # 7. generate random values row by row and write them into CSV file
    j = 0
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=delimiter, quoting=quoting)
        csv_writer.writerow(col_names)
        while j < rows:
            csv_writer.writerow([next(f) if isinstance(f, types.GeneratorType)
                                 else f() for f in generator_funcs])
            j += 1
            v_print("Printed line number:", j, end='\r')

    # 8. print input params to stdout for sanity check
    print("\n\nNumber of rows to print:", rows)
    print("Delimiter used:", delimiter)
    print("Quoting:", args.q)
    print("Data written to file:", output_file)


if __name__ == '__main__':
    # Note: To test inputs for flag 't', try this:
    # python generate_csv.py -t "int_id(5,2),str_id(8,10), ascii_str( 8, 12),utf8_str(8,12) , double (1.5 , 5.6 ), numeric( 10, 4 ),integer(-5 , 5000),date('2018-01-01','2019-12-12'),date_time('2018-01-01',"2019-12-12"), categorical("blah",'1',2, 3)"
    main()
