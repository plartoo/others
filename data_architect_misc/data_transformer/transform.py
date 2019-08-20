import pdb

import argparse
import os

import pandas as pd

import transform_errors
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
    parser = argparse.ArgumentParser(description=transform_utils.DESC)
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
        input_files = transform_utils.get_input_files(config)
        output_file_prefix = transform_utils.get_output_file_path_with_name_prefix(config)

        for input_file in input_files:
            col_names_from_input_file = transform_utils.get_raw_column_names(input_file, config)
            col_names_or_indexes_to_use = transform_utils.get_columns_to_use(config)


            if transform_utils.is_excel(input_file):
                sheet = transform_utils.get_sheet_index_or_name(config)
            elif transform_utils.is_csv(input_file):
                encoding = transform_utils.get_csv_encoding(config)
                input_csv_delimiter = transform_utils.get_csv_delimiter(config)
            else:
                raise transform_errors.InvalidFileType(input_file)



        # TODO: get column header row index or custom column headers to use
        cols_to_use = transform_utils.get_columns_to_use(config)
        # TODO: get column rename mappings
        leading_rows = transform_utils.get_leading_rows_to_skip(config)
        trailing_rows = transform_utils.get_trailing_rows_to_skip(config)




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


