""""
Description: Script to unzip raw weekly zip files from Sizmek global accounts;
extract account_id and account_name fields from file name;
insert these information into data frame; do some data transformation;
and output CSV file to be uploaded into Azure DB.

Last modified: July 11, 2019
"""
import csv
from glob import glob
import os
import re

import zipfile
import pandas as pd


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
        # print(zf, "\tread.")
        account_id, account_name = get_account_id_and_name(zf)
        # REF: https://stackoverflow.com/a/44080299
        with zipfile.ZipFile(zf, "r") as zip_ref:
            i =0
            for f in zip_ref.namelist():
                # print(f, "\tread.")
                i += 1
                output_file = os.path.join(output_dir,
                                           '--'.join([account_id, account_name, str(i)])
                                           + '.csv')

                with open(output_file, "wb") as fo:
                    fo.write(zip_ref.read(f))
                    print(output_file, "\twritten.")


def percent_to_float(data):
    return float(data.strip('%'))/100


def read_data(file_name, converters):
    df = pd.read_csv(file_name,
                     skiprows = 17,
                     skipfooter = 1,
                     engine = 'python',
                     converters = converters)
    return df


def add_columns(file_name, df):
    account_info = file_name.split('--')
    account_id = account_info[0]
    account_name = account_info[1]
    try:
        df.insert(loc = 1, column = 'AccountId', value = account_id)
        df.insert(loc = 2, column = 'AccountName', value = account_name)
        df.insert(loc = 29, column = 'OrderedImpressions', value = None)
    except e:
        pdb.set_trace()
        print('error')
    return df


def main():

    # 1. This step is for unzipping; commented out for now
    # input_zip_files = glob('*.zip')
    # output_dir = os.getcwd()
    # unzip_files(input_zip_files, output_dir)

    # 2. After unzipping files, apply transformation and save out as CSV
    unzipped_files = glob('*.csv')
    print("Total csv files:", len(unzipped_files))
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
        'Ad Average Duration (Sec)': 'Ad Average Duration_Sec',
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
        'Video Played with Sound Rate': 'VideoUnMutedRate',
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
        print("processing:", file_name)
        df = read_data(file_name, converters)
        if not df.empty:
            df = add_columns(file_name, df)
            df.rename(columns=cols_rename_dict, inplace=True)
            df.to_csv(''.join(['cleaned_', file_name,]),
                      quoting=csv.QUOTE_ALL,
                      index=False)


if __name__ == '__main__':
    main()
