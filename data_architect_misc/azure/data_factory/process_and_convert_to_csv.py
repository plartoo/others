import fnmatch
import json
import os
import shutil
import sys
import time
import uuid

import pandas as pd
from azure.storage.blob import BlockBlobService

STORAGE_ACCOUNT_NAME = ''
STORAGE_ACCOUNT_KEY = ''
OUTPUT_FILE_TYPE = '.txt' # Note: Never change this. We agreed to always output txt file

SHEET_NAME = 0 # 'None' to convert all sheets in the Excel file
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
        print("\nNew sys path appended:\n", sys.path, "\n")


def join_path_and_file_name(path, file_name, separator=os.sep):
    # Note: I can combine the following lines into one line of code,
    # but I won't because of better readability
    normalized_path = os.path.normpath(path)
    file_name_with_path = os.path.join(normalized_path, file_name).split(os.sep)
    return separator.join(file_name_with_path)


def read_excel_file(file_path_and_name, sheet_name=0, header=0,
                    skiprows=0, skipfooter=0):
    t1 = time.time()
    df = pd.read_excel(file_path_and_name, sheet_name=sheet_name,
                       header=header, skiprows=skiprows, skipfooter=skipfooter)
    print('Read Excel file:', file_path_and_name)
    print("It took this many seconds to read the file:", time.time() - t1, "\n")
    return df


def write_csv_file(data, output_file_path_and_name, sep=DELIMITER):
    t1 = time.time()
    data.to_csv(path_or_buf=output_file_path_and_name, sep=sep, index=False)
    print('Converted to CSV file and placed it here:', output_file_path_and_name)
    print("It took this many seconds to write the CSV file:", time.time() - t1, "\n")


# Does not work for files like: POL_N_S-PersonalCare_INV_KAN_20160101_20181130_20190117_EC.xlsx
# REF: https://stackoverflow.com/a/47558794/1330974
def get_active_sheet_name(excel_file_path_and_name):
    xl = xlrd.open_workbook(excel_file_path_and_name)
    for sht in xl.sheets():
        if sht.sheet_visible == 1:
            return sht.name


def get_value_from_dict(dict, key, default_value=''):
    if dict.get(key) is None:
        return default_value
    else:
        return dict.get(key)


def extract_file_name(blob_path_and_file_name):
    return os.path.split(blob_path_and_file_name)[-1]


def get_local_path_for_downloaded_blob_file(local_dir_name, blob_file_name):
    return os.path.join(local_dir_name, blob_file_name)


def download_blob_file_to_local_folder(block_blob_service, container_name, blob_file_with_path, local_file_with_path):
    block_blob_service.get_blob_to_path(container_name, blob_file_with_path, local_file_with_path)
    print("\nDownloaded:", blob_file_with_path, "and placed it here:", local_file_with_path)


def main():
    # 1. create local directory and append it to sys.path so that we can load Python modules in it later
    local_dir_name = str(uuid.uuid4())
    create_unique_local_download_directory(local_dir_name)
    append_new_sys_path(local_dir_name)

    """
    # The JSON below is only for testing on your laptop; on production environment, we'll use step 2a. instead
    json_activity = {'typeProperties': {'extendedProperties':
                                            {'sourceContainer': 'colgate-palmolive',
                                             'excelSourcePath': 'Test/Input',
                                             'fileName': 'IRP_N_ALL_*.xlsx',
                                             'uploadPath': 'Test/Output',
                                             'excelArchivePath': 'Test/Archive',
                                             'outputFileDelimiter': '|',
                                             #'sheetName': '',
                                             'skipHeaderRow': '0',
                                             'skipTrailingRow': '0',
                                             'additionalProcessingCode': '4_Python_Code/countries/india/*.py',
                                             }
                                        }
                     }
    """
    # 2a. get 'Extended Properties' passed from Azure Data Factory task
    read_activity = open('activity.json').read()
    json_activity = json.loads(read_activity)
    container_name = json_activity['typeProperties']['extendedProperties']['sourceContainer']
    path_to_source_blob_file = json_activity['typeProperties']['extendedProperties']['excelSourcePath']
    source_blob_file_name_or_pattern = json_activity['typeProperties']['extendedProperties']['fileName']
    upload_blob_location = json_activity['typeProperties']['extendedProperties']['uploadPath']
    archive_blob_location = json_activity['typeProperties']['extendedProperties']['excelArchivePath']

    # 2b. get Optional parameters from 'Extended Parameters' if they are provided
    delimiter = get_value_from_dict(json_activity['typeProperties']['extendedProperties'],
                                    'outputFileDelimiter',
                                    default_value=DELIMITER)
    sheet_name = get_value_from_dict(json_activity['typeProperties']['extendedProperties'],
                                     'sheetName',
                                     default_value=SHEET_NAME)
    header_rows_to_skip = int(get_value_from_dict(json_activity['typeProperties']['extendedProperties'],
                                    'skipHeaderRow',
                                    default_value=HEADER_ROWS_TO_SKIP))
    footer_rows_to_skip = int(get_value_from_dict(json_activity['typeProperties']['extendedProperties'],
                                    'skipTrailingRow',
                                    default_value=FOOTER_ROWS_TO_SKIP))
    additional_processing_code = get_value_from_dict(json_activity['typeProperties']['extendedProperties'],
                                    'additionalProcessingCode',
                                    default_value=None)
    print("Input parameters received:\n", json_activity)

    # 3. connect to blob
    block_blob_service = BlockBlobService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
    blob_content_generator = block_blob_service.list_blobs(container_name)
    blob_file_name_with_path = join_path_and_file_name(path_to_source_blob_file,
                                                       source_blob_file_name_or_pattern,
                                                       separator='/')

    # 4. if there's additional processing code, download them to local directory
    additional_processing_code_downloaded = []
    for blob in blob_content_generator:
        if (additional_processing_code is not None) and fnmatch.fnmatch(blob.name, additional_processing_code):
            blob_file_name = extract_file_name(blob.name)
            local_python_file_name_with_path = get_local_path_for_downloaded_blob_file(local_dir_name, blob_file_name)
            download_blob_file_to_local_folder(block_blob_service, container_name,
                                               blob.name, local_python_file_name_with_path)
            additional_processing_code_downloaded.append(local_python_file_name_with_path)

    # 5. if desired (matching) content in the blob is found
    for blob in blob_content_generator:
        if fnmatch.fnmatch(blob.name, blob_file_name_with_path):
            blob_file_name = extract_file_name(blob.name)
            local_excel_file_name_with_path = get_local_path_for_downloaded_blob_file(local_dir_name, blob_file_name)
            local_csv_file_name = ''.join([os.path.splitext(blob_file_name)[0], OUTPUT_FILE_TYPE])
            local_csv_file_name_with_path = os.path.join(local_dir_name, local_csv_file_name)

            # 6. download from the blob to local Excel file in a temp directory
            download_blob_file_to_local_folder(block_blob_service, container_name,
                                               blob.name, local_excel_file_name_with_path)

            # # Note: attempt to get the active sheet name; I don't like this, but team suggested this feature
            # # But both xlrd and openpyxl approaches failed
            # if sheet_name == 'choose-active-sheet':
            #     # a) xlrd approach fails because the flag isn't set properly for some Excel files
            #     sheet_name = get_active_sheet_name(local_excel_file_name_with_path)
            #     # b) openpyxl approach fails because it can't even handle file of size 13MB
            #     # wb = openpyxl.load_workbook(local_excel_file_name_with_path, read_only=True)
            #     # sheet_name = wb.active.title
            #     print("Choose this as active sheet:", sheet_name)

            if additional_processing_code_downloaded:
                # 7a. if we are told to load additional processing code, we load it here
                # Note: we can do dynamic loading here later based on file names like
                # this: https://stackoverflow.com/a/1057765
                # or this: https://stackoverflow.com/a/20753073
                # but for now, we will start with something simple
                import process_data as pcd
                df = pcd.process_data(local_excel_file_name_with_path)
            else:
                # 7b. if no custom processing is required, simply read from the local Excel file
                df = read_excel_file(local_excel_file_name_with_path,
                                     sheet_name=sheet_name,
                                     skiprows=header_rows_to_skip,
                                     skipfooter=footer_rows_to_skip)
            # 8. write the resulting (processed) data frame to csv
            # Note: if we want to enforce user to specify the sheet name, we can use this example:
            # https://stackoverflow.com/a/46081870/1330974
            write_csv_file(df, local_csv_file_name_with_path, delimiter)

            # 9. upload the csv to blob
            dest_blob_path_and_name = join_path_and_file_name(upload_blob_location, local_csv_file_name, separator='/')
            block_blob_service.create_blob_from_path(container_name,
                                                     dest_blob_path_and_name,
                                                     local_csv_file_name_with_path)
            print("Uploaded local csv file to destination blob:", dest_blob_path_and_name)

            # 10. move source blob to archive folder
            source_blob_url = block_blob_service.make_blob_url(container_name, blob.name)
            archive_blob_path_and_name = join_path_and_file_name(archive_blob_location, blob_file_name, separator='/')
            block_blob_service.copy_blob(container_name,
                                         archive_blob_path_and_name,
                                         source_blob_url)
            print("Copied source blob to archive blob location:", archive_blob_path_and_name)

            # 11. delete the old (source) blob
            block_blob_service.delete_blob(container_name, blob.name)
            print("Deleted source blob:", blob.name)

    # 12. delete local files and folder downloaded temporarily from Azure
    try:
        shutil.rmtree(local_dir_name)
        print("Deleted local folder and its contents:", local_dir_name)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


if __name__ == '__main__':
    main()
