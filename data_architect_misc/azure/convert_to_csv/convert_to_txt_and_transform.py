"""
Script to convert XLSX, XLS, XLSB and CSV files in
Azure blob to TXT files with delimiter (default is '|'),
and apply custom data processing function written in Python,
if any is provided, and put them back in the target Azure blob.

Author: Phyo Thiha
Last Modified: July 16, 2020
"""
import argparse
from datetime import datetime, timedelta
import fnmatch
import json
import importlib
import os
import shutil
import sys
import time
import uuid

# To get Azure storage SDK for Python, run this: pip install azure-storage-blob
# REF: https://docs.microsoft.com/en-us/python/api/overview/azure/storage-index?view=azure-python
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions
import pandas as pd

DESC = """
This script is used in our Azure Data Factory pipeline to 
convert raw input files, which are in xlsx, xls, xlsb or csv 
format and are located in Azure blob, to a text (.txt) file 
with delimiter (default delimiter is '|'). 

This script will return the blob path and file name of 
the converted txt file so that it will be available 
as the output of custom activity in the Azure Data Factory.
  
Before writing the input data to the output .txt file, 
this script loads the raw data as Pandas dataframe and 
also allows the caller (user of this code) to apply additional 
processing code (written in Python). This allows the caller 
to apply some basic data transformation to the original 
data (using Pandas dataframe as a base) before writing 
it to the output .txt file. 'transform_data.py' is an example 
script that shows how to write script to transform the original 
dataframe.  

Embed this script to be run on Azure Data Factory like this:
> python3 convert_to_txt_and_transform.py -adf 1

Or run this script on local machine using input flags like below:
> python convert_to_txt_and_transform.py
-adf 0                  (0 is for running from local machine. 1 is to be used in production 
                        such as Azure Data Factory or Azure Batch instance.) 
-sc 'colgate-palmolive' ([Required argument] blob container's name 
                        where input/source file is situated.)
-sp 'test/source_file'  ([Required argument] blob path for input/source file.)
-fn 'Belgium.xlsb'      ([Required argument] input/source file name.)
-sn 'Sheet1'            (sheet name, if the input/source file is Excel.
                        Default is 'Sheet1'.)
-id '|'                 (delimiter to use for the input file, if the input/source 
                        file is CSV. Default is '|'.)
-ie 'utf-8'             (encoding to use for the input file, if the input/source 
                        file is CSV. Default is 'utf-8'.)
-skr 0                  (skip header row, which means number of rows to skip at 
                        the top of the input file.)
-str 0                  (skip trailing row, which means number of rows to skip at 
                        the bottom of the input file.)
-ap 'test/archive_source'   ([Required argument] blob path to archive the source file; 
                            that is, the blob path to put the input/source file after 
                            converting it to .txt file.)
-op 'test/converted_file'   (blob path for the converted/output file.)
-od '|'                     (delimiter to use for output file. Default is '|'.)
-dtc 'test/python_scripts/transform_data.py' 
                            (blob path to Python script that accepts dataframe as input 
                            and apply necessary data transformation before writing the 
                            transformed data to the destination blob. The python script 
                            must implement 'transform_data' method that takes pandas 
                            dataframe as input and returns transformed pandas dataframe.
                            See 'transform_data.py' as an example.)

One-line example is:
> python convert_to_txt_and_transform.py -adf 0 -sc comp-harm -sp test/transformed_data/AED_GCC -fn Transformed_GCC_20200601_20200630__rows_0_225_20200729_123451.csv 
-id , -ap test/transformed_data/AED_GCC/archive_source -op test/transformed_data/AED_GCC/converted_txt -dtc python_scripts/transform_data.py
"""

STORAGE_PATH_SEPARATOR = '/'
STORAGE_ACCOUNT_NAME = 'wmdatarfcolgate'
STORAGE_ACCOUNT_URL = 'https://wmdatarfcolgate.blob.core.windows.net'
# Note: Enter your Azure blob storage key below or set it as an environment variable
# This is only required for local run. On ADF, we will use linked services to read the storage key dynamically
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

SAS_TOKEN = generate_account_sas(
    account_name=STORAGE_ACCOUNT_NAME,
    account_key=STORAGE_ACCOUNT_KEY,
    resource_types=ResourceTypes(service=True),
    permission=AccountSasPermissions(read=True),
    expiry=datetime.utcnow() + timedelta(hours=1)
)

# Important: NEVER change file extension other than '.txt' for comp harm project
OUTPUT_FILE_TYPE = '.txt'

REQUIRED_INPUT_ARGS = ['sc', 'sp', 'fn', 'ap', 'op']
# Note: If SHEET_NAME=None, then Pandas will convert all sheets in the Excel file
DEFAULT_SHEET_NAME = 'Sheet1'
DEFAULT_DELIMITER = '|'
DEFAULT_ENCODING = 'utf-8'
DEFAULT_HEADER_ROWS_TO_SKIP = 0
DEFAULT_FOOTER_ROWS_TO_SKIP = 0


def create_unique_local_download_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def add_directory_to_sys_path(dir_name):
    new_sys_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_name)
    if new_sys_path not in sys.path:
        sys.path.append(new_sys_path)
        print(f"New sys path appended: {new_sys_path}")
        print(f"to the current sys path which is:\n{sys.path}\n")


def join_path_and_file_name(path, file_name, separator=os.sep):
    # Note: I can combine the following lines into one line of code,
    # but I won't because of better readability
    normalized_path = os.path.normpath(path)
    file_name_with_path = os.path.join(normalized_path, file_name).split(os.sep)
    return separator.join(file_name_with_path)


def get_file_extension(file_path_and_name):
    return os.path.splitext(file_path_and_name)[-1]


def is_csv_file(file_path_and_name):
    return get_file_extension(file_path_and_name) == '.csv'


def is_xlsx_file(file_path_and_name):
    return get_file_extension(file_path_and_name) == '.xlsx'


def is_xls_file(file_path_and_name):
    return get_file_extension(file_path_and_name) == '.xls'


def is_xlsb_file(file_path_and_name):
    return get_file_extension(file_path_and_name) == '.xlsb'


def is_excel_file(file_path_and_name):
    return is_xlsx_file(file_path_and_name) \
           or is_xls_file(file_path_and_name) \
           or is_xlsb_file(file_path_and_name)


def get_excel_engine(file_path_and_name):
    # Based on the file extension, return the Excel engine to use
    if is_xlsx_file(file_path_and_name):
        return 'openpyxl'
    elif is_xls_file(file_path_and_name):
        return 'xlrd'
    elif is_xlsb_file(file_path_and_name):
        return 'pyxlsb'
    else:
        return None


def read_excel_file(file_path_and_name,
                    sheet_name,
                    skip_rows,
                    skip_footer,
                    header=0):
    t1 = time.time()
    engine = get_excel_engine(file_path_and_name)
    df = pd.read_excel(file_path_and_name,
                       sheet_name=sheet_name,
                       header=header,
                       skiprows=skip_rows,
                       skipfooter=skip_footer,
                       engine=engine)
    print(f"Reading Excel file: {file_path_and_name}")
    print(f"It took this many seconds to read the file above: {time.time() - t1}\n")
    return df


def read_csv_file(file_path_and_name,
                  input_delimiter,
                  input_encoding,
                  skip_rows,
                  skip_footer):
    t1 = time.time()
    df = pd.read_csv(file_path_and_name,
                     delimiter=input_delimiter,
                     skiprows=skip_rows,
                     skipfooter=skip_footer,
                     encoding=input_encoding)
    print(f"Reading CSV file: {file_path_and_name}")
    print(f"It took this many seconds to read the file above: {time.time() - t1}\n")
    return df


def read_data(file_path_and_name,
              sheet_name=DEFAULT_SHEET_NAME,
              input_delimiter=DEFAULT_DELIMITER,
              input_encoding=DEFAULT_ENCODING,
              skip_rows=DEFAULT_HEADER_ROWS_TO_SKIP,
              skip_footer=DEFAULT_FOOTER_ROWS_TO_SKIP
              ):
    if is_excel_file(file_path_and_name):
        # WARNING: Note that for xlsb files that have active cell
        # somewhere at the end of the file, pd.read_excel will
        # start reading from there (meaning, it will read mostly empty cells).
        # A way to fix this is to read xlsb data using xlwings, but
        # I highly suggest against using it because it's a semi-proprietary
        # library and launches an Excel workbook application, which is
        # unrealistic in our Linux environment. I have provided an example
        # of how to achieve reading only the cells with data using
        # xlwings at the end of this code file.
        return read_excel_file(file_path_and_name,
                               sheet_name,
                               skip_rows,
                               skip_footer)
    elif is_csv_file(file_path_and_name):
        return read_csv_file(file_path_and_name,
                             input_delimiter,
                             input_encoding,
                             skip_rows,
                             skip_footer)
    else:
        raise Exception(f"File type not supported for reading: {file_path_and_name}\n")


def write_output_file(
        dataframe,
        output_file_path_and_name,
        delimiter=DEFAULT_DELIMITER,
        encoding=DEFAULT_ENCODING
):
    t1 = time.time()
    dataframe.to_csv(
        path_or_buf=output_file_path_and_name,
        index=False,
        sep=delimiter,
        encoding=encoding)
    print(f"Writing the output dataframe to here: {output_file_path_and_name}")
    print(f"It took this many seconds to write the file: {time.time() - t1}\n")


def upload_local_file_to_blob(container_client, local_file, blob_path_and_file_name):
    with open(local_file, "rb") as data:
        container_client.upload_blob(blob_path_and_file_name, data)
        print(f"Uploaded local file to the destination blob: {blob_path_and_file_name}\n")


def download_blob_file_to_local(container_client, blob_name, local_path_and_file_name):
    with open(local_path_and_file_name, "wb") as my_blob:
        blob_data = container_client.download_blob(blob_name)
        blob_data.readinto(my_blob)
    print(f"Downloaded: {blob_name}\nand placed it here: {local_path_and_file_name}\n")


def extract_file_path_and_name(file_path_and_name):
    return (os.path.split(file_path_and_name)[0],
            os.path.split(file_path_and_name)[-1])


def get_absolute_module_name_out_of_file_path_and_name(file_path_and_name):
    # Replaces file path separators with '.' and then remove the file extension
    # E.g., 'folder1/folder2/transform_data.py' becomes 'folder1.folder2.transform_data'
    return os.path.splitext(file_path_and_name.replace(os.sep, '.'))[0]


def get_activity_config():
    activity = open('activity.json').read()
    activity_json = json.loads(activity)
    return activity_json.get('typeProperties').get('extendedProperties')


def get_blob_connection_string():
    linked_services = open('linkedServices.json').read()
    linked_services_json = json.loads(linked_services)
    return linked_services_json[0]['properties']['typeProperties']['connectionString']


def main():
    # 0. Extract input parameters for the program
    parser = argparse.ArgumentParser(
        description=DESC,
        formatter_class=argparse.RawTextHelpFormatter,
        usage=argparse.SUPPRESS)
    parser.add_argument('-adf', type=int, default=0,
                        help="Set this flag to 1 if this code is to be run in Azure Data Factory. "
                             "Set to 0 if to run on local machine. Default is 0.")
    parser.add_argument('-sc', type=str,
                        help="Source (blob) container name [e.g., 'colgate-palmolive']")
    parser.add_argument('-sp', type=str,
                        help="Source file's blob path [e.g., 'Test/Input']")
    parser.add_argument('-fn', type=str,
                        help="Source file's name [e.g., 'Belgium_Data.xlsx']")
    parser.add_argument('-sn', type=str, default=DEFAULT_SHEET_NAME,
                        help="Sheet name to read (if input file is an Excel file). Default is 'Sheet1'.")
    parser.add_argument('-id', type=str, default=DEFAULT_DELIMITER,
                        help="Delimiter to use in parsing the input file if it is CSV. Default is '|'.")
    parser.add_argument('-ie', type=str, default=DEFAULT_ENCODING,
                        help="Encoding to use for the input file, if the input/source file is CSV. "
                             "Default is 'utf-8'.")
    parser.add_argument('-skr', type=int, default=DEFAULT_HEADER_ROWS_TO_SKIP,
                        help="Number of header/leading rows to skip from the top of the input file in reading. "
                             "Default is 0.")
    parser.add_argument('-str', type=int, default=DEFAULT_FOOTER_ROWS_TO_SKIP,
                        help="Number of bottom/trailing rows to skip from the bottom of the input file in reading. "
                             "Default is 0")
    parser.add_argument('-ap', type=str,
                        help="Archive blob path to move the source file to after reading and processing. [e.g., "
                             "'Test/Archive']")
    parser.add_argument('-op', type=str,
                        help="Output blob path to write the processed/converted .txt file. [e.g., "
                             "'Test/Output']")
    parser.add_argument('-od', type=str, default=DEFAULT_DELIMITER,
                        help="Delimiter to use for the processed/converted .txt file. Default is '|'.")
    parser.add_argument('-dtc', type=str,
                        help="Full blob path of the data transform code (Python script that will be used to "
                             "transform the raw data). [e.g.,'Test/Python_Code/transform_belgium_data.py']")
    args = parser.parse_args()

    if args.adf == 0:
        for argk, argv in vars(args).items():
            # We unfortunately cannot use argparse's 'required=True' because this code is
            # intended to be run locally as well as in Azure Batch instances. In the latter,
            # using argparse's 'required' will cause issues in running this script.
            # That's why we have to check if input args are required or not like below.
            if (argk in REQUIRED_INPUT_ARGS) and (argv is None):
                raise Exception(f"Input parameter with flag, '{argk}', is required.")

        activity_config = {
            'sourceContainer': args.sc,
            'sourcePath': args.sp,
            'fileName': args.fn,
            'sheetName': args.sn,
            'inputCsvDelimiter': args.id,
            'inputCsvEncoding': args.ie,
            'skipHeaderRow': args.skr,
            'skipTrailingRow': args.str,
            'sourceArchivePath': args.ap,
            'outputPath': args.op,
            'outputCsvDelimiter': args.od,
            'dataTransformCodePathAndFileName': args.dtc,
        }
        # Connect to blob and create container client
        # REF: https://pypi.org/project/azure-storage-blob/
        # Alternative way to get blob service client is:
        # blob_service_client = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=SAS_TOKEN)
        blob_service_client = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=STORAGE_ACCOUNT_KEY)
    else:
        activity_config = get_activity_config()
        # On ADF, we'll dynamically fetch storage account key via Linked Services JSON
        blob_connection_string = get_blob_connection_string()
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)

    dest_blob_path_and_name = None
    source_container = activity_config.get('sourceContainer')
    source_path = activity_config.get('sourcePath')
    source_file_name = activity_config.get('fileName')
    sheet_name = activity_config.get('sheetName', DEFAULT_SHEET_NAME)
    input_delimiter = activity_config.get('inputCsvDelimiter', DEFAULT_DELIMITER)
    input_encoding = activity_config.get('inputCsvEncoding', DEFAULT_ENCODING)
    header_rows_to_skip = int(activity_config.get('skipHeaderRow', DEFAULT_HEADER_ROWS_TO_SKIP))
    footer_rows_to_skip = int(activity_config.get('skipTrailingRow', DEFAULT_FOOTER_ROWS_TO_SKIP))

    archive_path = activity_config.get('sourceArchivePath')
    output_path = activity_config.get('outputPath')
    output_delimiter = activity_config.get('outputCsvDelimiter', DEFAULT_DELIMITER)
    output_encoding = DEFAULT_ENCODING

    data_transform_script = activity_config.get('dataTransformCodePathAndFileName')
    print(f"Input parameters received:\n {json.dumps(activity_config, indent=4, sort_keys=True)}\n")

    # 1. Create local directory and append it to sys.path so that we can load Python modules in it later
    local_dir_name = str(uuid.uuid4())
    create_unique_local_download_directory(local_dir_name)
    add_directory_to_sys_path(local_dir_name)

    # 2. Create container client
    container_client = blob_service_client.get_container_client(source_container)
    blobs = [b for b in container_client.list_blobs()]

    # 3. If there's data transform code, download the code file to local directory and import the module in it
    # REF: How to import Python module - https://stackoverflow.com/a/54956419
    # data_transform_module = None
    # local_data_transform_code_path_and_file_name = None
    data_transform_module = None
    if data_transform_script:
        for blob in blobs:
            if fnmatch.fnmatch(blob.name, data_transform_script):
                _, cur_blob_file_name = extract_file_path_and_name(blob.name)
                local_data_transform_code_path_and_file_name = os.path.join(local_dir_name, cur_blob_file_name)
                download_blob_file_to_local(container_client, blob.name, local_data_transform_code_path_and_file_name)
                print(f"Found matching code file at: {blob.name}\nand downloaded it to: "
                      f"{local_data_transform_code_path_and_file_name}\n")

                data_transform_file_in_absolute_term = get_absolute_module_name_out_of_file_path_and_name(
                    local_data_transform_code_path_and_file_name)
                data_transform_module = importlib.import_module(data_transform_file_in_absolute_term)
                print(f"Imported this module: {data_transform_file_in_absolute_term}\n")

    # 4. Iterate over all existing blobs in the container to find matching blob name for the source (input) file
    source_blob_file_path_and_name = join_path_and_file_name(source_path,
                                                             source_file_name,
                                                             separator=STORAGE_PATH_SEPARATOR)

    for blob in blobs:
        if fnmatch.fnmatch(blob.name, source_blob_file_path_and_name):
            # 5. If source (input) file is found in the blob list,
            # download the blob and put it in a local temp directory created in step 1
            print(f"Found this blob as source file: {blob.name}\n")
            _, cur_blob_file_name = extract_file_path_and_name(blob.name)
            local_source_file_path_and_name = os.path.join(local_dir_name, cur_blob_file_name)
            download_blob_file_to_local(container_client, blob.name, local_source_file_path_and_name)
            df = read_data(local_source_file_path_and_name,
                           sheet_name=sheet_name,
                           input_delimiter=input_delimiter,
                           input_encoding=input_encoding,
                           skip_rows=header_rows_to_skip,
                           skip_footer=footer_rows_to_skip)

            if data_transform_module is not None:
                # 6. Apply data transformation function, transform_data(),
                # from data transform module to the dataframe.
                df = data_transform_module.transform_data(df)
                print(
                    f"Successfully applied data transformation code: {local_data_transform_code_path_and_file_name}\n")

            # 7. Write the (transformed) dataframe as local txt file
            local_txt_file_name = ''.join([os.path.splitext(cur_blob_file_name)[0], OUTPUT_FILE_TYPE])
            local_txt_file_path_and_name = os.path.join(local_dir_name, local_txt_file_name)
            write_output_file(df,
                              local_txt_file_path_and_name,
                              delimiter=output_delimiter,
                              encoding=output_encoding)

            # 8. Upload the (converted) local csv file to blob destination
            dest_blob_path_and_name = join_path_and_file_name(output_path,
                                                              local_txt_file_name,
                                                              separator=STORAGE_PATH_SEPARATOR)
            print(f"Uploading converted txt file to blob.")
            upload_local_file_to_blob(container_client,
                                      local_txt_file_path_and_name,
                                      dest_blob_path_and_name)

            # Step 9 and 10 can be completed by ADF, so we'll comment them out
            # 9. Archive source file (i.e. copy source file in the local temp folder to the blob archive folder)
            archive_blob_path_and_name = join_path_and_file_name(archive_path,
                                                                 cur_blob_file_name,
                                                                 separator=STORAGE_PATH_SEPARATOR)
            print(f"Copying source file to blob's archive location.")
            upload_local_file_to_blob(container_client,
                                      local_source_file_path_and_name,
                                      archive_blob_path_and_name)

            # 10. Delete the source blob
            container_client.delete_blob(blob.name)
            print(f"Deleted source blob: {blob.name}")

    # 12. Delete the local folder and files downloaded temporarily from Azure blob
    try:
        shutil.rmtree(local_dir_name)
        print(f"Deleted local (temp) folder and its contents: {local_dir_name}\n")
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}\n")

    print(f"Writing blob path and file name of the converted file (to be used in Custom Activity of ADF) to "
          f"'outputs.json' file: {dest_blob_path_and_name}")
    output_dict = {'dest_blob_path_and_name': dest_blob_path_and_name}
    with open('outputs.json', 'w') as outfile:  # writing values to custom output
        json.dump(output_dict, outfile)

    return


if __name__ == '__main__':
    main()

# For my team and other readers, this is how to read data cells that are NOT empty using xlwings:
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
