import pdb

import argparse
import json
import os
import sys

import pandas as pd
import xlrd # As of April 2020, Pandas still uses xlrd to read Excel (xls and xlsx) files.
import openpyxl # Excel file writing engine for Pandas' to_excel function.

import transform_errors
import transform_functions
import transform_utils


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

        # TODO: We need to think about renaming this transform_funcs_instance as custom_module_instance
        # because we might want to use this pattern for logging; QA-ing and mapping tasks
        #
        # Before writing custom functions to transform data, please read
        # https://archive.st/7w9d (also available at: http://archive.ph/qXKXC)
        transform_funcs_instance = transform_utils.instantiate_transform_functions_module(config)

        row_idx_where_data_starts = transform_utils.get_row_index_where_data_starts(config)
        footer_rows_to_skip = transform_utils.get_number_of_rows_to_skip_from_bottom(config)

        for input_file in transform_utils.get_input_files(config):
            print("Processing file:", input_file)
            # TODO: Time the performance and log it
            # t1 = time.time()
            # print('Read Excel file:', file_path_and_name)
            # print("It took this many seconds to read the file:", time.time() - t1, "\n")

            # TODO: maybe combine get_raw_column_headers with read_data because I use the latter just for the former
            col_headers_from_input_file = transform_utils.get_raw_column_headers(input_file, config)

            if transform_utils.is_excel(input_file):
                sheet = transform_utils.get_input_file_sheet_name(config)
                keep_default_na = transform_utils.get_keep_default_na(config)
                # Note: We will load everything on the sheet in Excel (i.e. no chunk processing).
                # Excel, theoretically, can store up to a maximum of:
                # 1048576 (rows) * 16384 (cols) 32767 (chars/cell) * 32 (bits/char for encoding like UTF-8)
                # = 4.5 petabytes of data, but we sure shouldn't be processing a file of such size
                # using this program nor no one in their right mind should be storing that much
                # data in an Excel file.

                # TODO: try out different Excel files to see how this skipping rows work
                print("\nSkipping this many rows (including header row) from the top of the file:",
                      row_idx_where_data_starts)
                cur_df = pd.read_excel(input_file,
                                       sheet_name=sheet,
                                       keep_default_na=keep_default_na,
                                       skiprows=row_idx_where_data_starts,
                                       skipfooter=footer_rows_to_skip,
                                       header=None,
                                       names=col_headers_from_input_file
                                       )

                for func_and_params in transform_utils.get_functions_to_apply(config):
                    print("\n=> Invoking transform function:\n", json.dumps(func_and_params,
                                                                          sort_keys=True,
                                                                          indent=4))
                    func_name = transform_utils.get_function_name(func_and_params)
                    func_args = transform_utils.get_function_args(func_and_params)
                    func_kwargs = transform_utils.get_function_kwargs(func_and_params)
                    cur_df = getattr(transform_funcs_instance,
                                     func_name)(cur_df, *func_args, **func_kwargs)
                    # print(cur_df)
                    # if func_name == 'update_str_value_in_col2_if_col1_has_one_of_given_values':
                    #     cur_df.to_excel('shit.xlsx', index=False)
                    #     sys.exit()
                    #     import pdb
                    #     pdb.set_trace()
                    #     print('debug')

                    # TODO: Logging, Mapping, CSV handling
                    # TODO: investigate by measuring memory usage (e.g., using memory_profiler like this: https://stackoverflow.com/a/41813238/1330974)
                    # if passing df in/out of function is memory expensive

                    # if transform_utils.KEY_TRANSFORM_FUNC_NAME in func_and_params:
                    #     # REF1: https://stackoverflow.com/a/12025554
                    #     # REF2: Partial approach - https://stackoverflow.com/a/56675539/1330974
                    #     # REF3: Passing variable length args in getattr - https://stackoverflow.com/q/6321940
                    #     print("=>Invoking transform function:", func_and_params)
                    #     func_args = transform_utils.get_transform_function_args(func_and_params)
                    #     func_kwargs = transform_utils.get_transform_function_kwargs(func_and_params)
                    #     cur_df = getattr(custom_funcs_instance,
                    #                      transform_utils.get_transform_function_name(
                    #                          func_and_params))(cur_df,*func_args,**func_kwargs)
                    #     import pdb
                    #     pdb.set_trace()
                    #     print('transform func')
                    # elif transform_utils.KEY_ASSERT_FUNC_NAME in func_and_params:
                    #     # and if not, merge assert and transform
                    #     # if so, ask question on SO like this: "Is passing around dataframes into functions in pandas memory intensive/expensive?"
                    #     print("=>Invoking assert function:", func_and_params)
                    #     func_args = transform_utils.get_assert_function_args(func_and_params)
                    #     func_kwargs = transform_utils.get_assert_function_kwargs(func_and_params)
                    #     getattr(custom_funcs_instance,
                    #             transform_utils.get_assert_function_name(
                    #                 func_and_params))(cur_df, *func_args, **func_kwargs)
                    #     import pdb
                    #     pdb.set_trace()
                    #     print('assert func')



            elif transform_utils.is_csv(input_file):
                # REF: how to chunk process CSV files https://pythonspeed.com/articles/chunking-pandas/
                rows_per_chunk = transform_utils.get_rows_per_chunk_for_csv(config)
                encoding = transform_utils.get_input_csv_encoding(config)
                input_csv_delimiter = transform_utils.get_input_csv_delimiter(config)
            else:
                raise transform_errors.InvalidFileType(input_file)


            if transform_utils.get_write_data_decision(config):
                dwm = transform_utils.instantiate_data_writer_module(config)
                dwm.write_data(cur_df)

        # 1. Read data in chunk (skipping x top rows; capturing header)
        # 2. For each chunk
        #   apply original column names to the chunk
        #   choose only columns to use
        #   rename columns if necessary
        #   apply functions (add columns, etc.)
        # df = pd.read_excel(input_file,sheet_name=sheet)

        print('Program finished.')
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


