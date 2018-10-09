import pdb

import argparse

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
>> python clean_data.py -i <raw_data_file.xlsx> -c <config_file.json>
'''

CHUNK_SIZE = 100000 # 100k chunks
## TODO: replace ',' with '.'
## remove headers and footers if any
## pivot

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('-c', required=True, type=str,
                        help="(Required) Full path and name of the JSON configuration file. "
                             "E.g., python clean_data.py -c .\configs\data_cleaning_config.json -i ...")
    parser.add_argument('-i', required=True, type=str,
                        help="(Required) FULL path and name of the input file. "
                             "E.g., python clean_data.py -i .\input\data_cleaning_config.json -c ...")
    args = parser.parse_args()
    config = load_config(args.c)
    extn = get_file_extension(args.i)

    # REF: https://stackoverflow.com/q/14262433
    if extn == 'xlsx':
        # REF: https://stackoverflow.com/a/44549301
        xlsx = pd.read_excel(args.i, sheetname=None)
        # read sheet by sheet as df and pass them onto the function
        sheets = xlsx.sheet_names

        for sheet in xlsx.
        pass
    elif extn == 'csv':
        #read chunk by chunk as df and pass them onto the function
        pass
    else:
        print("Raw data file extension type is not supported.")
        exit(1)

    df = pd.read
    # get extension
    # if XLSX
    # read sheet by sheet
    # if CSV
    # read file in chunk
    # get headers
    # skip rows
    #
    # skip footers
    pdb.set_trace()
    print("Finished cleaning data.")