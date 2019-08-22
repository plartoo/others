""""
Authors: Phyo Thiha and Edgar Cervantes
Last modified: August 13, 2019

Description: Script to run on Azure Batch account to unzip
raw weekly zip files from Sizmek global accounts; extract
account_id and account_name fields from file name;
insert these information into data frame; do some data
transformation; and output CSV file to be uploaded into
Azure SQL Server.
"""

import csv
import datetime
from glob import glob
import fnmatch
import os
import re
import json
import zipfile
import pandas as pd
import numpy as np
import uuid
import sys
import shutil
from azure.storage.blob import BlockBlobService

STORAGE_ACCOUNT_NAME = 'enter accnt name here'
STORAGE_ACCOUNT_KEY = 'enter accnt key here'

DATA_TYPES = {
'Campaign ID': str,
'Campaign Name': str,
'Advertiser ID': str,
'Advertiser Name': str,
'Cost-Based Type': str,
'Site ID': str,
'Site Name': str,
'Unit Cost': float,
'Unit Size': str,
'Package Name': str,
'Placement ID': str,
'Placement Name': str,
'Placement Type': str,
'Placement Classification 1': str,
'Placement Classification 2': str,
'Placement Classification 3': str,
'Placement Classification 4': str,
'Placement Classification 5': str,
'* Served Impressions': int,
'Unique Impressions': int,
'Ad Average Duration (Sec)': float,
'eCPC': float,
'* Clicks': int,
'Interactions': int,
'Total Media Cost': float,
'Total Actions': int,
'Unique Video Viewers': int,
'Average Frequency': float,
'eCPM': float,
'eCPA': float,
'Total Conversions': int,
'Video Started': int,
'Video Played 25%': int,
'Video Played 50%': int,
'Video Played 75%': int,
'Video Fully Played': int,
'Video Played with Sound': int,
'Impressions with Video Start': int
}

def create_unique_local_download_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def append_new_sys_path(dir_name):
    new_sys_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_name)
    if new_sys_path not in sys.path:
        sys.path.append(new_sys_path)
        print("\nNew sys path appended:", new_sys_path)
        print("Current sys path is:\n", sys.path, "\n")

def extract_file_name(blob_path_and_file_name):
    return os.path.split(blob_path_and_file_name)[-1]

def get_local_path_for_downloaded_blob_file(local_dir_name, blob_file_name):
    return os.path.join(local_dir_name, blob_file_name)

def join_path_and_file_name(path, file_name, separator=os.sep):
    # Note: I can combine the following lines into one line of code,
    # but I won't because of better readability
    normalized_path = os.path.normpath(path)
    file_name_with_path = os.path.join(normalized_path, file_name).split(os.sep)
    return separator.join(file_name_with_path)

def download_blob_file_to_local_folder(block_blob_service, container_name, blob_file_with_path, local_file_with_path):
    block_blob_service.get_blob_to_path(container_name, blob_file_with_path, local_file_with_path)
    print("\nDownloaded:", blob_file_with_path, "and placed it here:", local_file_with_path)

class ReportDateRangeError(Exception):
    pass

def get_account_id_and_name(zip_file_name):
    account_id = re.findall(r'_(\d+)\-', zip_file_name)[0]
    if re.findall(r'.*\d+\-(.*-)_?_Custom_Report', zip_file_name):
        # for '70c09efd-cbf4-4889-be5c-6fb03e9cfaee_129286-Colgate_Palmolive_SE_-__Custom_Report_080424_31374217'
        # or '811e1cac-0771-4967-ab92-4c15f81e72a6_122329-Colgate_Palmolive_PAN_-_Custom_Report_080750_31374295'
        matched_part = re.findall(r'.*\d+\-(.*-)_?_Custom_Report',
                                  zip_file_name)[0]
        account_name = ''.join([matched_part.replace('_',' '),' MEC'])
    elif re.findall(r'.*\d+\-([^-]+)_Custom_Report',zip_file_name):
        matched_part = re.findall(r'.*\d+\-([^-]+)_Custom_Report',
                                  zip_file_name)[0]
        if matched_part.endswith('_'):
            # for 'bc24f68f-1058-47de-8c89-8d6b43606179_134570-Colgate_Palmolive_APAC__Custom_Report_080722_31374291'
            account_name = ''.join([matched_part.replace('_',' '),' MEC'])
        else:
            # for 'cc7337dc-af2c-49d4-8580-c831185591eb_76314-MEC_Colgate_Puerto_Rico_Custom_Report_080843_31373531'
            account_name = matched_part.replace('_', ' ')
    return account_id, account_name


def unzip_files(zip_files, output_dir):
    for zf in zip_files:
        account_id, account_name = get_account_id_and_name(zf)
        uniqueFileCode = re.findall(r'(.*?)_', os.path.split(zf)[1])
        # REF: https://stackoverflow.com/a/44080299
        with zipfile.ZipFile(zf, "r") as zip_ref:
            i =0
            for f in zip_ref.namelist():
                i += 1
                output_file = os.path.join(output_dir,
                                           '--'.join([uniqueFileCode[0], account_id, account_name, str(i)])
                                           + '.csv')

                with open(output_file, "wb") as fo:
                    fo.write(zip_ref.read(f))


def percent_to_float(data):
    return float(data.strip('%'))/100


def read_data(file_name, converters, skiprows=0, skipfooter=0):
    df = pd.read_csv(file_name,
                     skiprows = skiprows,
                     skipfooter = skipfooter,
                     dtype=DATA_TYPES,
                     thousands=',',
                     engine = 'python',
                     converters = converters)
    return df


def extract_report_date_range_str(file_name):
    # try to detect 'Report Date Range' from the first 100 lines of the CSV report
    df = pd.read_csv(file_name, header=None, usecols=[0], skiprows=0, nrows=100)
    for i, row in df.iterrows():
        row_str = str(row[0])
        if re.search(r'report date range', row_str, re.I):
            date_range = re.search(r'report date range.*\((.*)\)', row_str, re.I)[1]
            dates = date_range.split('-')
            ranges = list(map(lambda x: datetime.datetime.strptime(x.strip(), '%m/%d/%Y').strftime('%Y%m%d'), dates))

    if (ranges is None) or (len(ranges) < 2):
        raise ReportDateRangeError("")
    else:
        return ranges


def add_columns(file_name, df):
    account_info = file_name.split('--')
    account_id = account_info[1]
    account_name = account_info[2]
    try:
        df.insert(loc = 1, column = 'AccountId', value = account_id)
        df.insert(loc = 2, column = 'AccountName', value = account_name)
        df.insert(loc = 29, column = 'OrderedImpressions', value = np.nan) # set OrderedImpressions to NULL
    except e:
        print(e)
    return df


def main():

	# 0. create local directory and append it to sys.path so that we can work with files at a local level
    local_dir_name = str(uuid.uuid4())
    create_unique_local_download_directory(local_dir_name)
    append_new_sys_path(local_dir_name)

	# 1. get 'Extended Properties' passed from Azure Data Factory task
    read_activity = open('activity.json').read()
    json_activity = json.loads(read_activity)
    # The JSON below is only for testing locally.
    #json_activity = {'typeProperties': {'extendedProperties':
    #                                        {'rawZippedFilesExtWildcard': '*.zip',
    #                                         'rawZippedFilesPath': 'sizmek/raw_zipped',#'0_Raw_Data/India/0_Raw_Files', #
    #                                         'cleanedFilesPath': 'sizmek/transformed',#'0_Raw_Data/India/1_Cleaned_Files_To_Upload', #
    #                                         'blobContainer': 'global-digital'#'0_Raw_Data/India/0_Raw_Files/Archive',#
    #                                         }
    #                                    }
    #                 }
    #"""

    rawZippedFilesExtWildcard = json_activity['typeProperties']['extendedProperties']['rawZippedFilesExtWildcard']
    rawZippedFilesPath = json_activity['typeProperties']['extendedProperties']['rawZippedFilesPath']
    cleanedFilesPath = json_activity['typeProperties']['extendedProperties']['cleanedFilesPath']
    blobContainer = json_activity['typeProperties']['extendedProperties']['blobContainer']
    print("Input parameters received:\n", json_activity)

	# 2. This step is for unzipping
    blob_service = BlockBlobService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
    zippedFiles_List = blob_service.list_blobs(blobContainer, prefix=rawZippedFilesPath)
    
    #Look for all the files and download them locally to unzip them
    for blob in zippedFiles_List:
        if fnmatch.fnmatch(blob.name, rawZippedFilesExtWildcard):
            blob_file_name = extract_file_name(blob.name)
            local_python_file_name_with_path = get_local_path_for_downloaded_blob_file(local_dir_name, blob_file_name)
            download_blob_file_to_local_folder(blob_service, blobContainer, blob.name, local_python_file_name_with_path)
            print("\nFound zip file at:", blob.name, "\nand downloaded it to:", local_python_file_name_with_path)
            #Look for the file locally and unzip it
            input_zip_files = glob(os.path.join(local_dir_name, '*.zip'))
            unzip_files(input_zip_files, local_dir_name)

    #Count total files that were unzziped and print message
    unzipped_files = glob(os.path.join(local_dir_name, '*.csv'))
    print("Total csv files:", len(unzipped_files))
  
    # 3. After unzipping files, we apply transformation and save out as CSV
    cols_rename_dict = {
        'Campaign ID': 'CampaignID',
        'Campaign Name': 'CampaignName',
        'Campaign Start Date': 'CampaignStartDate',
        'Campaign End Date': 'CampaignEndDate',
        'Advertiser ID': 'AdvertiserID',
        'Advertiser Name': 'AdvertiserName',
        'Cost-Based Type': 'CostTypeName',
        'Site ID': 'SiteID',
        'Site Name': 'SiteName',
        'Unit Cost': 'CostPerUnit',
        'Unit Size': 'UnitSize',
        'Package Start Date': 'PackageStartDate',
        'Package Start Date - Actual': 'PackageActualStartDate',
        'Package End Date': 'PackageEndDate',
        'Package Name': 'PackageName',
        'Placement ID': 'PlacementID',
        'Placement Name': 'PlacementName',
        'Placement Start Date': 'PlacementStartDate',
        'Placement Start Date - Actual': 'PlacementActualStartDate',
        'Placement End Date': 'PlacementEndDate',
        'Placement Type': 'PlacementType',
        'Placement Classification 1': 'PlacementClassification1',
        'Placement Classification 2': 'PlacementClassification2',
        'Placement Classification 3': 'PlacementClassification3',
        'Placement Classification 4': 'PlacementClassification4',
        'Placement Classification 5': 'PlacementClassification5',
        '* Served Impressions': 'ServedImpressions',
        'Unique Impressions': 'UniqueImpressions',
        'Ad Average Duration (Sec)': 'AdAverageDurationSec',
        'eCPC': 'ECPC',
        '* Clicks': 'Clicks',
        '* CTR': 'CTR',
        'Total Media Cost': 'TotalMediaCost',
        'Total Actions': 'TotalActions',
        'Unique Video Viewers': 'UniqueVideoViewers',
        'Average Frequency': 'AverageFrequency',
        'Total Conversions': 'TotalConversions',
        'Conversion Rate': 'ConversionRate',
        'Video Started': 'VideoStarted',
        'Video Played 25%': 'VideoPlayed25',
        'Video Played 50%': 'VideoPlayed50',
        'Video Played 75%': 'VideoPlayed75',
        'Video Fully Played': 'VideoFullyPlayed',
        'Video Played with Sound': 'VideoPlayedWithSound',
        'Video Started Rate': 'VideoStartedRate',
        'Video 25% Played Rate': 'Video25Rate',
        'Video 50% Played Rate': 'Video50Rate',
        'Video 75% Played Rate': 'Video75Rate',
        'Video Fully Played Rate': 'VideoFullyPlayedRate',
        'Video Played with Sound Rate': 'VideoPlayedWithSoundRate',
        'Impressions with Video Start': 'ImpressionsWithVideoStart'
    }
    converters = {
        '* CTR': percent_to_float,
        'Conversion Rate': percent_to_float,
        'Video Started Rate': percent_to_float,
        'Video 25% Played Rate': percent_to_float,
        'Video 50% Played Rate': percent_to_float,
        'Video 75% Played Rate': percent_to_float,
        'Video Fully Played Rate': percent_to_float,
        'Video Played with Sound Rate': percent_to_float,
    }
    for file_name in unzipped_files:
        print("processing unzip file:", file_name)
        start_date, end_date = extract_report_date_range_str(file_name)
        df = read_data(file_name, converters, 17, 1)
        if not df.empty:
            df = add_columns(file_name, df)
            df.rename(columns=cols_rename_dict, inplace=True)
            #creates the cleaned csv file
            print('new name: ' + '_'.join(['Cleaned', start_date, end_date, os.path.split(file_name)[1],]))
            df.to_csv(os.path.join(local_dir_name, '_'.join(['Cleaned', start_date, end_date, os.path.split(file_name)[1],])),
                      quoting=csv.QUOTE_MINIMAL,
                      sep='|',
                      index=False)
    
    #Count total files that were cleaned and print message
    cleaned_files = glob(os.path.join(local_dir_name, 'Cleaned*.csv'))
    print("Total cleaned files:", len(cleaned_files))

    # 4. upload cleaned files to blob
    for cleanedFile in cleaned_files:
        dest_blob_path_and_name = join_path_and_file_name(cleanedFilesPath, os.path.split(cleanedFile)[1], separator='/')
        blob_service.create_blob_from_path(blobContainer, dest_blob_path_and_name, cleanedFile)
        print("Uploaded local cleaned file: " + os.path.split(cleanedFile)[1] + " to destination blob: " + cleanedFilesPath)

    # 5. delete local files and folder downloaded temporarily from Azure
    try:
        shutil.rmtree(local_dir_name)
        print("Deleted local folder and its content:", local_dir_name)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

if __name__ == '__main__':
    main()
