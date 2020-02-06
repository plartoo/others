import pdb

import argparse
import os
import sys

import pandas as pd

import transform_errors
import transform_functions
import transform_utils

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
    # 1. Process arguments passed into the program
    parser = argparse.ArgumentParser(description=transform_utils.DESC,
                                     formatter_class = argparse.RawTextHelpFormatter,
                                     usage=argparse.SUPPRESS)
    parser.add_argument('-c', required=True, type=str,
                        help=transform_utils.HELP)
    args = parser.parse_args()

    # 2. Load JSON configuration file
    if (not args.c) or (not os.path.exists(args.c)):
        raise transform_errors.ConfigFileError()

    # 3. Iterate through each transform procedure in config file
    for config in transform_utils.load_config(args.c):
        # Make sure config JSON has no conflicting keys and invalid data types
        transform_utils.validate_configurations(config)
        output_file_prefix = transform_utils.get_output_file_path_with_name_prefix(config)
        custom_funcs_module = transform_utils.load_custom_functions(config)
        custom_funcs = transform_utils.get_functions_to_apply(config)

        row_idx_where_data_starts = transform_utils.get_row_index_where_data_starts(config)
        footer_rows_to_skip = transform_utils.get_number_of_rows_to_skip_from_bottom(config)

        for input_file in transform_utils.get_input_files(config):
            print("Processing file:", input_file)
            # t1 = time.time()
            # print('Read Excel file:', file_path_and_name)
            # print("It took this many seconds to read the file:", time.time() - t1, "\n")

            # TODO: maybe combine get_raw_column_headers with read_data because I use the latter just for the former
            col_headers_from_input_file = transform_utils.get_raw_column_headers(input_file, config)

            if transform_utils.is_excel(input_file):
                sheet = transform_utils.get_sheet_name(config)
                # Note: We will load everything on the sheet in Excel (i.e. no chunk processing)
                # because anybody reasonable would not be using Excel to store terabytes of data.
                # Excel, theoretically, can store up to maximum of:
                # 1048576 (rows) * 16384 (cols) 32767 (chars/cell) * 32 (bits/char for encoding like UTF-8)
                # = 4.5 petabytes of data, but we sure shouldn't be processing a file of such size
                # using this program

                # TODO: try out different Excel files to see how this skipping rows work
                print("Skipping this many rows:", row_idx_where_data_starts)
                df_raw = pd.read_excel(input_file,
                                       sheet_name=sheet,
                                       skiprows=row_idx_where_data_starts,
                                       skipfooter=footer_rows_to_skip,
                                       header=None,
                                       names=col_headers_from_input_file
                                       )


                # TODO: We need to think about renaming this transform_funcs as custom_modules
                # because we might want to use this pattern for logging; QA-ing and mapping tasks
                #
                # Before writing custom functions to transform data, please read
                # https://archive.st/7w9d (also available at: http://archive.ph/qXKXC)
                #
                custom_funcs_instance = custom_funcs_module.CountrySpecificTransformFunctions()
                # drop_columns(df, [])
                # stack_columns(df)
                # add_compete_non_compete_flag(df, [])
                custom_funcs_instance.call_swiss()
                custom_funcs_instance.parent_function()
                # TOCONT: use partial to create a function for each of the ones in custom_funcs list and call them
                import pdb
                pdb.set_trace()
                # We need to apply these rules:
                # 1. rename columns
                # 2. drop columns
                # 3.
                print('debug')

            elif transform_utils.is_csv(input_file):
                rows_per_chunk = transform_utils.get_rows_per_chunk_for_csv(config)
                encoding = transform_utils.get_input_csv_encoding(config)
                input_csv_delimiter = transform_utils.get_input_csv_delimiter(config)
            else:
                raise transform_errors.InvalidFileType(input_file)



        # 1. Read data in chunk (skipping x top rows; capturing header)
        # 2. For each chunk
        #   apply original column names to the chunk
        #   choose only columns to use
        #   rename columns if necessary
        #   apply functions (add columns, etc.)
        # df = pd.read_excel(input_file,sheet_name=sheet)
        pdb.set_trace()
        print('haha')
        #     df = transform_utils.get_data_frame()
        #
        # For CSV,
        # how to read the header row
        # df1 = pd.read_csv('test.csv',skiprows=3,nrows=1)
        # how to read the rest of data frames
        # df1 = pd.read_csv('test.csv',header=None,skiprows=rows_to_skip+header_row_if_any)

    # REF: reduce memory use Pandas: https://towardsdatascience.com/why-and-how-to-use-pandas-with-large-data-9594dda2ea4c
    #https://www.giacomodebidda.com/reading-large-excel-files-with-pandas/
    # REF: pandas snippets: https://jeffdelaney.me/blog/useful-snippets-in-pandas/
    # # REF: https://stackoverflow.com/q/14262433
    # Drop columns
    # https://cmdlinetips.com/2018/04/how-to-drop-one-or-more-columns-in-pandas-dataframe/
    # extn = get_file_extension(args.i)
    # if extn == '.xlsx':
    #     # REF: https://stackoverflow.com/a/44549301
    #     xlsx = pd.read_excel(args.i, sheet_name=None,
    #                          skiprows=cc.LEADING_ROWS_TO_SKIP,
    #                          skipfooter=cc.BOTTOM_ROWS_TO_SKIP)
    #     for sheet_name, cur_df in xlsx.items():
    #         # read sheet by sheet as df and pass them onto the function
    #         pdb.set_trace()
    #         # df.to_dict(orient='records')
    #         pass
    #
    # elif extn == '.csv':
    #     if cc.BOTTOM_ROWS_TO_SKIP > 0:
    #         # Pandas doesn't allow skipping footers if we process things in
    #         # chunk, so we handle this special case here
    #         cur_df = pd.read_csv(args.i,
    #                              skiprows=cc.LEADING_ROWS_TO_SKIP,
    #                              skipfooter=cc.BOTTOM_ROWS_TO_SKIP)
    #         pdb.set_trace()
    #     else:
    #         # otherwise, read by chunk and do further processing
    #         for cur_df in pd.read_csv(args.i, chunksize=CHUNK_SIZE,
    #                                   skiprows=cc.LEADING_ROWS_TO_SKIP):
    #             pdb.set_trace()
    #             pass
    # else:
    #     print("Raw data file type is not supported.")
    #     exit(1)
    #
    #


