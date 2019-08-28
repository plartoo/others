import pdb
import transform_errors
import transform_utils

import pandas as pd

if __name__ == '__main__':
    fn = 'csv.csv'
    chunksize = 5 # rows_to_read
    row_index_where_data_starts = 1
    trailing_rows = 0 # skip_trailing_rows; MUST always be 0 for chunk reading
    row_index_to_extract_column_names = 0
    custom_header_names = None
    column_names_or_indexes_to_use = None
    custom_data_types = {}
    config = {
        'sheet_name_of_excel_file': 'Sheet1',
        'input_csv_file_encoding': 'utf-8',
        'input_csv_file_delimiter': '|',
    }

    # for chunk in transform_utils.read_data(
    #     fn,
    #     config,
    #     chunk, # rows_to_read
    #     skip_leading_rows=row_index_where_data_starts,
    #     skip_trailing_rows=trailing_rows, # skipfooter is NOT supported in chunk (if we put other than 0 here, it'll raise error)
    #     header_row_index=row_index_to_extract_column_names,
    #     custom_header_names=custom_header_names,
    #     column_names_or_indexes_to_use=column_names_or_indexes_to_use,
    #     custom_data_types=custom_data_types
    # ):
    #     print(chunk)

    # for chunk in pd.read_csv(
    #     'csv.csv',
    #     skiprows=0, # row_index_where_data_starts, # so we cannot default this to '1'; we must default this to '0'
    #     chunksize=chunksize,
    #     skipfooter=0,
    #     header=row_index_to_extract_column_names,
    #     names=custom_header_names,
    #     usecols=column_names_or_indexes_to_use,
    #     dtype={},
    #     delimiter='|',
    #     encoding='utf-8'):
    #     print(chunk)
    #
    # print("\n====\n")

    # for chunk in pd.read_csv(
    #     'csv_no_header.csv',
    #     skiprows=0,# row_index_where_data_starts,
    #     chunksize=chunksize,
    #     skipfooter=0,
    #     header=None,# if there is no header, we have to set this to None
    #     names=custom_header_names,
    #     usecols=column_names_or_indexes_to_use,
    #     dtype={},
    #     delimiter='|',
    #     encoding='utf-8'):
    #     print(chunk)
    # print("\n====\n")


    # # this is how to read accounting for the header row
    # # header is on rw num #5, data starts at row num #9
    # for chunk in pd.read_csv(
    #     'csvv.csv',
    #     skiprows=4,# row_index_where_data_starts,
    #     chunksize=chunksize,
    #     skipfooter=0,
    #     header=0,# if there is no header, we have to set this to None
    #     names=custom_header_names,
    #     usecols=column_names_or_indexes_to_use,
    #     dtype={},
    #     delimiter='|',
    #     encoding='utf-8'):
    #     print(chunk)
    # print("\n====\n")


    # ## GOOD TO GO for csv
    # # how to read WIHTOUT including header row
    # # header is on rw num #5, data starts at row num #9
    # for chunk in pd.read_csv(
    #     'csvv.csv',
    #     skiprows=8,# row_index_where_data_starts,
    #     chunksize=chunksize,
    #     #skipfooter=0,
    #     header=None,# if there is no header, we have to set this to None
    #     names=custom_header_names,
    #     usecols=column_names_or_indexes_to_use,
    #     dtype={},
    #     delimiter='|',
    #     encoding='utf-8'):
    #     if chunk.shape[0] < chunksize:
    #         chunk.drop(chunk.tail(2).index, inplace=True)
    #     print(chunk)
    #     print(chunk.shape[0])
    # print("\n====\n")
    #
    # # WITHOUT assuming header row
    # for chunk in pd.read_csv(
    #         'csv_no_header.csv',
    #         skiprows=0,# row_index_where_data_starts,
    #         chunksize=chunksize,
    #         #skipfooter=0,
    #         header=None,# if there is no header, we have to set this to None
    #         names=custom_header_names,
    #         usecols=column_names_or_indexes_to_use,
    #         dtype={},
    #         delimiter='|',
    #         encoding='utf-8'):
    #     print(chunk)
    #     print(chunk.shape[0])
    # print("\n====\n")
    #
    # # WITHOUT assuming header row
    # for chunk in pd.read_csv(
    #     'csv.csv',
    #     skiprows=1, # row_index_where_data_starts, # so we cannot default this to '1'; we must default this to '0'
    #     chunksize=chunksize,
    #     #skipfooter=0,
    #     header=None,
    #     names=custom_header_names,
    #     usecols=column_names_or_indexes_to_use,
    #     dtype={},
    #     delimiter='|',
    #     encoding='utf-8'):
    #     print(chunk)
    #     print(chunk.shape[0])
    #
    # print("\n====\n")

    # how to read WIHTOUT including header row
    # header is on rw num #5, data starts at row num #9
    for chunk in pd.read_excel(
        'excell.xlsx',
        skiprows=8,# row_index_where_data_starts,
        nrows=chunksize,
        header=None,# if there is no header, we have to set this to None
        names=custom_header_names,
        usecols=column_names_or_indexes_to_use,
        dtype={},
        delimiter='|',
        encoding='utf-8'):
        if chunk.shape[0] < chunksize:
            chunk.drop(chunk.tail(2).index, inplace=True)
        print(chunk)
        print(chunk.shape[0])
    print("\n====\n")

    # # WITHOUT assuming header row
    # for chunk in pd.read_excel(
    #         'excel_no_header.xlsx',
    #         skiprows=0,# row_index_where_data_starts,
    #         chunksize=chunksize,
    #         header=None,# if there is no header, we have to set this to None
    #         names=custom_header_names,
    #         usecols=column_names_or_indexes_to_use,
    #         dtype={},
    #         delimiter='|',
    #         encoding='utf-8'):
    #     print(chunk)
    #     print(chunk.shape[0])
    # print("\n====\n")
    #
    # # WITHOUT assuming header row
    # for chunk in pd.read_excel(
    #     'excel.xlsx',
    #     skiprows=1, # row_index_where_data_starts, # so we cannot default this to '1'; we must default this to '0'
    #     chunksize=chunksize,
    #     header=None,
    #     names=custom_header_names,
    #     usecols=column_names_or_indexes_to_use,
    #     dtype={},
    #     delimiter='|',
    #     encoding='utf-8'):
    #     print(chunk)
    #     print(chunk.shape[0])

    print("\n====\n")

# Possible Approaches
# 1. convert XLSX to CSV and then consolidate read_data into that
# 2. read ALL (max possible) lines in XLSX
# 3. Find out row number in Excel file and use nrows to read chunk by chunk
