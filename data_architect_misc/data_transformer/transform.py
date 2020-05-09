"""
Read 'DESC' in the code below to see what this script is for.

Author: Phyo Thiha
Last Modified Date: May 8, 2020
"""

import argparse
import datetime
import dateutil.relativedelta
import logging
import os
import sys

from data_readers.file_data_reader import FileDataReader
import transform_errors
import transform_utils


DESC = """This program is intended to take a JSON configuration file 
(e.g., config.json) as its input. In that JSON config file, user can 
define as instructions (such as location of the input raw data file,  
where to write the output data to, etc.) as well as functions and 
their associated parameters to be applied to and checked against the 
input data. The processed/QA-ed data, if instructed in the config 
file, can be written to an output CSV/Excel file or to a SQL Server 
table or any other custom destination (such as Azure Blob, Amazon S3, 
etc) as programmed in a custom writer module.
\nUsage example #1 - If the input file's path and name are defined
in the config file, run the program like below:
    >> python transform.py -c .\configs\china\config.json

\nUsage example #2 - Alternatively input file's path and name can be 
provided with 'i' flag to the program as below:
    >> python transform.py -c .\configs\china\config.json 
    -i ./input/switzerland/Monthly_Spend_20200229.xlsx"""

C_FLAG_HELP_TEXT = """[Required] Configuration file (with full or relative path).
E.g., python transform.py -c .\configs\china\config.json"""

I_FLAG_HELP_TEXT = """[Optional] Input file (with full or relative path) that 
has data to which the functions defined in the config file will be applied to.
E.g., python transform.py -i ./input/switzerland/Monthly_Spend_20200229.xlsx 
-c .\configs\china\config.json"""

if __name__ == '__main__':
    # 0. Set logging config
    # REF 1: https://stackoverflow.com/a/15729700/1330974
    # REF 2a: https://web.archive.org/save/https://www.loggly.com/ultimate-guide/python-logging-basics/
    # REF 2b: http://archive.ph/0Uf6u
    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format="\n%(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)  # ('transform.py')

    # 1. Process arguments passed into the program
    parser = argparse.ArgumentParser(
        description=DESC,
        formatter_class=argparse.RawTextHelpFormatter,
        usage=argparse.SUPPRESS)
    parser.add_argument('-c', required=True, type=str,
                        help=C_FLAG_HELP_TEXT)
    parser.add_argument('-i', required=False, type=str,
                        help=I_FLAG_HELP_TEXT)
    args = parser.parse_args()

    # 2. Make sure JSON configuration file exists
    if not os.path.exists(args.c):
        raise transform_errors.ConfigFileError()

    # 3. Iterate through each transform procedure in config file
    start_dt = datetime.datetime.now()
    for config in transform_utils.load_config(args.c):
        if args.i:
            # This hack allows user to provide input file as commandline parameter
            config = transform_utils.insert_input_file_keys_values_to_config_json(args.i, config)

        # Make sure config JSON has no conflicting keys and invalid data types
        transform_utils.validate_configurations(config)

        for input_file in transform_utils.get_input_files(config):
            reader = FileDataReader(input_file, config).get_data_reader()
            write_data = transform_utils.get_write_data_decision(config)
            data_writer_kls = transform_utils.instantiate_data_writer_class(config)
            # To optimize the application of custom function to Pandas' dataframe, read:
            # REF: https://archive.st/7w9d (also available at: http://archive.ph/qXKXC)
            transform_funcs_kls = transform_utils.instantiate_transform_functions_class(config)

            row_count = 0
            cur_df = reader.read_next_dataframe()
            while not cur_df.empty:
                for func_and_params in transform_utils.get_functions_to_apply(config):
                    # logger.info(f"Invoking function:{json.dumps(func_and_params, sort_keys=True, indent=4)}")
                    logger.info(f"Invoking function: {func_and_params['function_name']}")
                    func_name = transform_utils.get_function_name(func_and_params)
                    func_args = transform_utils.get_function_args(func_and_params)
                    func_kwargs = transform_utils.get_function_kwargs(func_and_params)
                    cur_df = getattr(transform_funcs_kls,
                                     func_name)(cur_df, *func_args, **func_kwargs)

                if write_data:
                    data_writer_kls.set_output_file_name_suffix(
                        f"rows_{row_count}_{row_count+cur_df.shape[0]}")
                    row_count = row_count+cur_df.shape[0]
                    data_writer_kls.write_data(cur_df)

                cur_df = reader.read_next_dataframe()

        td = dateutil.relativedelta.relativedelta (datetime.datetime.now(), start_dt)
        logger.info(f"Transform script finished and from start to completion it took "
                    f"{td.hours} hrs, {td.minutes} mins, and {td.seconds} secs.")

    # TODO : use pydoc to generate documentation?
    # >> python -m pydoc -w transform

    # To reduce memory usage in Pandas:
    # https://towardsdatascience.com/why-and-how-to-use-pandas-with-large-data-9594dda2ea4c
    # https://www.giacomodebidda.com/reading-large-excel-files-with-pandas/

    # To measure RAM (memory) usage using memory profiler (I already did)
    # https://stackoverflow.com/a/41813238/1330974

    # REFs related to reading data by chunk in Pandas:
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#iterating-through-files-chunk-by-chunk

    # Other useful REFs related to Pandas:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
    # https://cmdlinetips.com/2018/04/how-to-drop-one-or-more-columns-in-pandas-dataframe/
    # https://jeffdelaney.me/blog/useful-snippets-in-pandas/
    # https://www.giacomodebidda.com/reading-large-excel-files-with-pandas/
    # https://stackoverflow.com/q/14262433
