import pdb

import argparse
import os
import sys

import pandas as pd

from file_utils import get_file_extension
from data_cleaning_utils import load_config

DESC = '''
This program cleans raw data files according to the rules set forth in the JSON configuration file.
Specifically, it will take only the raw columns speficied in the JSON config file, and rename them
to the processed (final) column names.  While doing so, it'll make sure that the data types, the 
format/string pattern and null replacements etc. in every row of the raw data are according to 
what is specified in the config file.

The output of this script is a TSV file with the raw data cleaned per config specification.

To find out how to run, use '-h' flag. Usage example:
>> python clean_data.py -i <raw_data_file.xlsx> -c <folder_where cleaning_config.py exists>

Specifically,
>> python clean_data.py -c .\configs\nic -i .\input\csv_test_with_blank_headers.csv
'''

CHUNK_SIZE = 100000 # 100k chunks
## ***TODO: replace ',' with '.'
# get extension
## remove headers and footers if any
# skip rows
# skip footers

# if XLSX
# read sheet by sheet
# if CSV
# read file in chunk

# get headers

## pivot

def check_data_against_rules(df, rules):
    replace_commas = rules['replace_commas_with_decimal_for_numbers']

    # [DM_1219_ColgateGlobal].[STG].[Data_Cleansing_Rule]
    # TODO: upper, ltrim, rtrim
    # "replace_commas_with_decimal_for_numbers": false,
    # Setting the whole column such as 'SUBMEDIA_1' or 'SUBMEDIA_2' as 'N/A' regardless of the condition
    # Delete rows that were loaded with null values for advertiser and local_spend (1. mark as delete if condition met)
    # Setting DAYPART = 'N/A' for records with a media type other than Radio or Television (2. if condition in one column is met, then apply something to another column)
    # Set TOTAL_DURATION = 0 for records having 'PRESS' as media type (see #2)
    # Delete records having a investment = 0 and Rating = 0 (3. mark as delete if condition in TWO columns is met)
    # Set spot_length = Total_Duration Field Spot_Length (4. Copy value from one column to another)
    # Replace all the NULL and empty values with N/A OR 0 Field SECTOR => ("default_value": "N/A" or "0")
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('-c', required=True, type=str,
                        help="(Required) (Full or relative) Path to the configuration file (which must be named 'config.py'). "
                             "E.g., python clean_data.py -c .\configs\nicaguara -i ...")
    parser.add_argument('-i', required=True, type=str,
                        help="(Required) (Full or relative) path AND name of the input data file. "
                             "E.g., python clean_data.py -i .\input\data.csv -c ...")
    args = parser.parse_args()

    # Dynamically load the config file
    # REF: https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
    # Other ways to import custom modules
    # REF: https://docs.python.org/3/library/importlib.html
    if (not args.c) or (not os.path.isdir(args.c)):
        sys.exit("You must provide a valid path to the configuration file")
    sys.path.append(args.c)
    import cleaning_config as cc
    pdb.set_trace()
    # REF: https://stackoverflow.com/q/14262433
    extn = get_file_extension(args.i)
    if extn == '.xlsx':
        # REF: https://stackoverflow.com/a/44549301
        xlsx = pd.read_excel(args.i, sheet_name=None,
                             skiprows=cc.LEADING_ROWS_TO_SKIP,
                             skipfooter=cc.BOTTOM_ROWS_TO_SKIP)
        for sheet_name, cur_df in xlsx.items():
            # read sheet by sheet as df and pass them onto the function
            pdb.set_trace()
            # df.to_dict(orient='records')
            pass

    elif extn == '.csv':
        if cc.BOTTOM_ROWS_TO_SKIP > 0:
            # Pandas doesn't allow skipping footers if we process things in
            # chunk, so we handle this special case here
            cur_df = pd.read_csv(args.i,
                                 skiprows=cc.LEADING_ROWS_TO_SKIP,
                                 skipfooter=cc.BOTTOM_ROWS_TO_SKIP)
            pdb.set_trace()
        else:
            # otherwise, read by chunk and do further processing
            for cur_df in pd.read_csv(args.i, chunksize=CHUNK_SIZE,
                                      skiprows=cc.LEADING_ROWS_TO_SKIP):
                pdb.set_trace()
                pass
    else:
        print("Raw data file type is not supported.")
        exit(1)


    # pdb.set_trace()
    print("Finished cleaning data.")
