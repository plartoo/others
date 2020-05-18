"""
Script to convert XLSX, XLS, XLSB files in Azure blob
to CSV file, apply custom processing functions, if
any is provided, and put them back in Azure blob
destination.

Author: Phyo Thiha
Last Modified: May 16, 2020
"""
from datetime import datetime, timedelta
import fnmatch
import json
import importlib
import os
import shutil
import sys
import time
import uuid

import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, generate_account_sas, ResourceTypes, AccountSasPermissions

STORAGE_ACCOUNT_NAME = 'wmdatarfcolgate'
STORAGE_ACCOUNT_URL = 'https://wmdatarfcolgate.blob.core.windows.net'
STORAGE_ACCOUNT_KEY = ''

SAS_TOKEN = generate_account_sas(
    account_name=STORAGE_ACCOUNT_NAME,
    account_key=STORAGE_ACCOUNT_KEY,
    resource_types=ResourceTypes(service=True),
    permission=AccountSasPermissions(read=True),
    expiry=datetime.utcnow() + timedelta(hours=1)
)

# Note: Never change this from '.txt' extension for comp harm project.
OUTPUT_FILE_TYPE = '.txt'

XLSB_ENGINE = 'pyxlsb'
XLS_ENGINE = 'xlrd'
XLSX_ENGINE = 'openpyxl'

# If SHEET_NAME=None, then Pandas will convert all sheets in the Excel file
SHEET_NAME = 0
DELIMITER = '|'
HEADER_ROWS_TO_SKIP = 0
FOOTER_ROWS_TO_SKIP = 0


def create_unique_local_download_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def append_new_sys_path(dir_name):
    new_sys_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_name)
    if new_sys_path not in sys.path:
        sys.path.append(new_sys_path)
        print(f"New sys path appended: {new_sys_path}")
        print(f"Current sys path is:\n{sys.path}\n")


def join_path_and_file_name(path, file_name, separator=os.sep):
    # Note: I can combine the following lines into one line of code,
    # but I won't because of better readability
    normalized_path = os.path.normpath(path)
    file_name_with_path = os.path.join(normalized_path, file_name).split(os.sep)
    return separator.join(file_name_with_path)


def read_excel_file(file_path_and_name,
                    sheet_name=0,
                    header=0,
                    skiprows=0,
                    skipfooter=0):

    t1 = time.time()
    engine = None
    if os.path.splitext(file_path_and_name)[-1] == '.xlsb':
        engine = XLSB_ENGINE
    elif os.path.splitext(file_path_and_name)[-1] == '.xls':
        engine = XLS_ENGINE
    elif os.path.splitext(file_path_and_name)[-1] == '.xlsx':
        engine = XLSX_ENGINE

    df1 = pd.read_excel(file_path_and_name,
                        sheet_name=sheet_name,
                        header=header,
                        skiprows=skiprows,
                        skipfooter=skipfooter,
                        engine=engine)
    print(f"Read Excel file: {file_path_and_name}")
    print(f"It took this many seconds to read the file: {time.time() - t1}\n")
    return df1


def write_csv_file(data, output_file_path_and_name, sep=DELIMITER):
    t1 = time.time()
    data.to_csv(path_or_buf=output_file_path_and_name, sep=sep, index=False, encoding='utf-8')
    print(f"Converted to CSV file and placed it here: {output_file_path_and_name}")
    print(f"It took this many seconds to write the CSV file: {time.time() - t1}\n")


def upload_local_file_to_blob(container_client, local_file, dest_blob_path_and_name):
    with open(local_file, "rb") as data:
        container_client.upload_blob(dest_blob_path_and_name, data)
        print(f"Uploaded local file to destination blob: {dest_blob_path_and_name}")


def extract_file_name_and_path(file_path_and_name):
    return (os.path.split(file_path_and_name)[0],
            os.path.split(file_path_and_name)[-1])


def get_local_destination_path_for_file(local_dir_name, file_name):
    """Join local path and downloaded blob file name."""
    return os.path.join(local_dir_name, file_name)


def download_blob_file_to_local_folder(container_client, blob_name, local_file_with_path):
    with open(local_file_with_path, "wb") as my_blob:
        blob_data = container_client.download_blob(blob_name)
        blob_data.readinto(my_blob)
    print(f"\nDownloaded: {blob_name}\nand placed it here: {local_file_with_path}\n")


def main():
    # 1. create local directory and append it to sys.path so that we can load Python modules in it later
    local_dir_name = str(uuid.uuid4())
    create_unique_local_download_directory(local_dir_name)
    append_new_sys_path(local_dir_name)

    # Note: comment out two lines below and replace it with json_activity variable below in local testing
    read_activity = open('activity.json').read()
    json_activity = json.loads(read_activity)
    # # The JSON below is only for testing on your laptop; on production environment, we'll use step 2a. instead
    # json_activity = {'typeProperties': {'extendedProperties':
    #                                         {'sourceContainer': 'colgate-palmolive',
    #                                          'excelSourcePath': 'Test/Input', #
    #                                          'fileName': 'Belgium.xlsb', #'argentina.xls',
    #                                          'uploadPath': 'Test/Output', #
    #                                          'excelArchivePath': 'Test/Archive',#
    #                                          'outputFileDelimiter': '|',
    #                                          # 'sheetName': '',
    #                                          'skipHeaderRow': '0',
    #                                          'skipTrailingRow': '0',
    #                                          'additionalProcessingCode': '4_Python_Code/Countries/Argentina/process_data_argentina.py'
    #                                          }
    #                                     }
    #                  }

    # 2a. Get required config for this script from 'Extended Properties' passed from Azure Data Factory task
    config_dict = json_activity.get('typeProperties').get('extendedProperties')
    container_name = config_dict.get('sourceContainer')
    path_to_source_blob_file = config_dict.get('excelSourcePath')
    source_blob_file_name_or_pattern = config_dict.get('fileName')
    upload_blob_location = config_dict.get('uploadPath')
    archive_blob_location = config_dict.get('excelArchivePath')

    # 2b. Get optional config for this script from 'Extended Properties' passed from Azure Data Factory task
    delimiter = config_dict.get('outputFileDelimiter', DELIMITER)
    sheet_name = config_dict.get('sheetName', SHEET_NAME)
    header_rows_to_skip = int(config_dict.get('skipHeaderRow', HEADER_ROWS_TO_SKIP))
    footer_rows_to_skip = int(config_dict.get('skipTrailingRow', FOOTER_ROWS_TO_SKIP))
    additional_processing_code = config_dict.get('additionalProcessingCode')
    print(f"Input parameters received:\n {json.dumps(config_dict, indent=4, sort_keys=True)}")

    # 3. Connect to blob
    # REF: https://pypi.org/project/azure-storage-blob/
    # Alternative way to get blob service client is:
    # blob_service_client = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=SAS_TOKEN)
    blob_service_client = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=STORAGE_ACCOUNT_KEY)

    container_client = blob_service_client.get_container_client(container_name)
    blobs = [b for b in container_client.list_blobs()]

    # 4. If there's additional processing code, download the code file to local directory and import the module in it
    # How to import Python module: https://stackoverflow.com/a/54956419
    custom_processing_module = None
    local_python_file_name_with_path = None
    if additional_processing_code is not None:
        for blob in blobs:
            if fnmatch.fnmatch(blob.name, additional_processing_code):
                _, cur_blob_file_name = extract_file_name_and_path(blob.name)
                local_python_file_name_with_path = get_local_destination_path_for_file(local_dir_name,
                                                                                       cur_blob_file_name)
                download_blob_file_to_local_folder(container_client, blob.name, local_python_file_name_with_path)
                print(f"Found matching code file at: {blob.name}\nand downloaded it to: "
                      f"{local_python_file_name_with_path}")
                file_path_and_name_without_extension = os.path.splitext(cur_blob_file_name)[0]
                custom_processing_module = importlib.import_module(os.path.join(file_path_and_name_without_extension))
                print(f"Imported this module: {file_path_and_name_without_extension}")

    target_blob_file_name_with_path = join_path_and_file_name(path_to_source_blob_file,
                                                              source_blob_file_name_or_pattern,
                                                              separator='/')
    # 5. Iterate over all existing blobs in the container
    for blob in blobs:
        cur_blob_file_path, cur_blob_file_name = extract_file_name_and_path(blob.name)
        target_blob_file_path, target_blob_file_name = extract_file_name_and_path(target_blob_file_name_with_path)
        if fnmatch.fnmatch(cur_blob_file_path, target_blob_file_path) \
                and fnmatch.fnmatch(cur_blob_file_name, target_blob_file_name):

            # 6. If desired (matching) content in the blob is found,
            # download the blob and put it in a temp directory in local destination
            local_excel_file_name_with_path = get_local_destination_path_for_file(local_dir_name, cur_blob_file_name)
            download_blob_file_to_local_folder(container_client, blob.name, local_excel_file_name_with_path)

            # WARNING: Note that for xlsb files that have active cell
            # somewhere at the end of the file, pd.read_excel will
            # start reading from there (meaning, read mostly empty cells).
            # A way to fix this is to read xlsb data using xlwings, but
            # I highly suggest against using it because it's a semi-proprietary
            # library and launches an Excel workbook application, which is
            # unrealistic in our Linux environment. I have provided an example
            # of how to achieve reading only the cells with data using
            # xlwings at the end of this code.
            df = read_excel_file(local_excel_file_name_with_path,
                                 sheet_name=sheet_name,
                                 skiprows=header_rows_to_skip,
                                 skipfooter=footer_rows_to_skip)

            if custom_processing_module is not None:
                # 7. If we need to apply functions from custom module to the dataframe, do it below
                df = custom_processing_module.process_data(df)
                print(f"Ran custom module: {local_python_file_name_with_path}\n successfully.\n")

            # 8. Write the downloaded (and processed) dataframe as local csv file
            # Note: if we want to enforce user to specify the sheet name, we can use this example:
            # https://stackoverflow.com/a/46081870/1330974
            local_csv_file_name = ''.join([os.path.splitext(cur_blob_file_name)[0], OUTPUT_FILE_TYPE])
            local_csv_file_name_with_path = os.path.join(local_dir_name, local_csv_file_name)
            write_csv_file(df, local_csv_file_name_with_path, delimiter)

            # 9. Upload the (converted) local csv file to blob destination
            dest_blob_path_and_name = join_path_and_file_name(upload_blob_location,
                                                              local_csv_file_name,
                                                              separator='/')
            upload_local_file_to_blob(container_client,
                                      local_csv_file_name_with_path,
                                      dest_blob_path_and_name)

            # 10. Copy original (before-conversion) file in local temp folder to to blob archive folder
            archive_blob_path_and_name = join_path_and_file_name(archive_blob_location,
                                                                 cur_blob_file_name,
                                                                 separator='/')
            upload_local_file_to_blob(container_client,
                                      local_excel_file_name_with_path,
                                      archive_blob_path_and_name)

            # 11. Delete the old (source) blob
            container_client.delete_blob(blob.name)
            print(f"Deleted source blob: {blob.name}")

    # 12. delete local files and folder downloaded temporarily from Azure
    try:
        shutil.rmtree(local_dir_name)
        print(f"Deleted local folder and its contents: {local_dir_name}")
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}")


if __name__ == '__main__':
    main()

# # How to read data cells that are NOT empty using xlwings
# import xlwings as xw
# book = xw.Book('Belgium.xlsb')
# first_sheet = book.sheets(1) #active_sheet=book.sheets.active
# # first_sheet.cells.last_cell.row is how to get the total rows
# # in an Excel sheet, which we already know as ~1+million rows
# # used_row_count = sum(x is not None for x in first_sheet.range('A:A').value)
# used_range_rows = (first_sheet.api.UsedRange.Row, first_sheet.api.UsedRange.Rows.Count)
# used_range_cols = (first_sheet.api.UsedRange.Column, first_sheet.api.UsedRange.Columns.Count)
# used_range = xw.Range(*zip(used_range_rows, used_range_cols)) # used_range.select()
# data = first_sheet.range(used_range).value
# df = pd.DataFrame(data[1:],columns=data[0])
