"""
Author: Phyo Thiha
Last Modified: September 13, 2019
Description: This is to calculate DMA weights (indexes) for
individual networks (Market_Monthly_Trend), for each market based on
national ratings (Network_Monthly_Trend), both of which we have
downloaded using Selenium.

IMPORTANT NOTE: Before running this script, we must create a mapping
file between network names in Market Monthly Trend and Network Monthly Trend
files. Use 'create_mappings.py' script to generate that file, and
ONLY AFTER THAT, run this script.
"""

import pdb

from datetime import datetime
import re
import os
import sys

import pandas as pd


# Placeholder keyword used when we cannot find matching national network (short) names
PLACEHOLDER = 'Not Available'
# Column name in the mapping file where we put short names of networks
SHORT_NAME_COLUMN = 'National Network Short Names'

INPUT_FOLDER = os.path.join(os.getcwd(), 'selenium_output')  # this is where selenium process dumps files
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'index_calculation_output')
PARTIAL_MAPPING_FILE_NAME = 'network_mappings'
PARTIAL_NETWORK_MONTHLY_TREND_FILE_NAME = 'Network_Monthly_Trend'
PARTIAL_MARKET_MONTHLY_TREND_FILE_NAME = 'Market_Monthly_Trend'


def create_output_folder(output_folder):
    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


def get_network_name(file_path_and_name):
    # Extract network names from row#3 of RenTrak Market Monthly Trend Excel files
    df = pd.read_excel(file_path_and_name, nrows=1, skiprows=2)
    return df.columns[0].split(',')[0].strip()


def split_files_by_year(list_of_files):
    # We will split files by their date range (year) and process each batch of files
    # That way, each output CSV files would have data for only one year.
    date_ranges = set()
    for f in list_of_files:
        date_ranges.add(re.search(r'(\d{8}_\d{8})__',f)[1])

    date_range_and_files = {}
    for d in date_ranges:
        date_range_and_files[d] = [f for f in list_of_files if d in f]
    return date_range_and_files


def main():
    create_output_folder(OUTPUT_FOLDER)

    # Step 1: Load mappings between individual network files (Market Monthly Trend) and
    # national network files (Network Monthly Trend).
    network_mapping_file = [os.path.join(INPUT_FOLDER,f) for f in os.listdir(INPUT_FOLDER)
                            if (os.path.isfile(os.path.join(INPUT_FOLDER, f)) and PARTIAL_MAPPING_FILE_NAME in f)]
    if not network_mapping_file:
        err_msg = ''.join(["ERROR: Before running this script, you must generate network_mappings.csv file using "
                           "'create_mappings.py'; manually review the output file; and place it here:", INPUT_FOLDER])
        sys.exit(err_msg)
    elif len(network_mapping_file) > 1:
        err_msg = ''.join(["ERROR: Found more than one mapping file. There must be only one (final) "
                           "mapping files in this folder:", INPUT_FOLDER])
        sys.exit(err_msg)
    else:
        print("\nLoading mapping file:", network_mapping_file[0])
        mappings_df = pd.read_csv(network_mapping_file[0], index_col=0)

    # Step 2: Build national consolidated data frame (clean ‘-‘, take out parens and put them as separate columns)
    # Select files which starts with 'Network_Monthly_Trend*' in the input folder
    national_rating_files = [os.path.join(INPUT_FOLDER,f) for f in os.listdir(INPUT_FOLDER)
                             if (os.path.isfile(os.path.join(INPUT_FOLDER, f)) and PARTIAL_NETWORK_MONTHLY_TREND_FILE_NAME in f)]
    dfs = []
    for f in national_rating_files:
        print("\nLoading national rating file:", f)
        df = pd.read_excel(f, na_values="-", index_col=0, skiprows=5, skipfooter=6)
        df.columns = [df.columns[0]] + [datetime.strptime(c.replace("\n",' '), '%b \'%y').strftime('%Y-%m') for c in df.columns[1:]]
        dfs.append(df)

    # Consolidate/merge all national ratings in one data frame
    national_ratings_df = pd.concat(dfs, axis=1, sort=False)
    national_ratings_df = national_ratings_df.groupby(national_ratings_df.columns, axis=1).first()#.fillna('')

    # Update network short names as indexes, and add original (full) network names as a new column.
    # Short names are like 'ABCFAM' for 'ABC Family' because these codes are what we care in analysis and indexing
    network_full_names = list(national_ratings_df.index)
    # Note: Below, we take [-1], the last match, because there are networks with two parentheses such as
    #  'BYU Television (Cable) (BYU-C)', 'V-me TV (Cable) (V-ME Cable)', 'GOL TV (Spanish) (GOL TVS)', etc.
    network_short_names =  [re.findall(r'\((.*?)\)', n)[-1] for n in network_full_names]
    national_ratings_df.index = network_short_names
    national_ratings_df.insert(0, "NetworkFullName", network_full_names, allow_duplicates=True)

    # Re-arrange columns so that NetworkFullName and Genre are the first ones (just because of my OCD)
    date_cols = [c for c in national_ratings_df.columns if re.search(r'\d{4}\-\d{2}', c)]
    non_date_cols = [c for c in national_ratings_df.columns if not re.search(r'\d{4}\-\d{2}', c)]
    national_ratings_df = national_ratings_df[non_date_cols + date_cols]

    market_files_by_date = split_files_by_year([os.path.join(INPUT_FOLDER,f) for f in os.listdir(INPUT_FOLDER)
                                                if (os.path.isfile(os.path.join(INPUT_FOLDER, f))
                                                    and PARTIAL_MARKET_MONTHLY_TREND_FILE_NAME in f)])

    # Step 3: Go through individual market monthly files and find corresponding period's and
    # market's national ratings from network monthly files to calculate the indexes.
    for d, files in market_files_by_date.items():
        output_file_name = ''.join(['rating_indexes_', d, '.csv'])

        rating_indexes = []
        for f in files:
            print("\nLoading market rating file:", f)
            network_name = get_network_name(f)
            print("Network name from Market file:", network_name)

            try:
                df = pd.read_excel(f, na_values="-", index_col=1, skiprows=5, skipfooter=6)
            except IndexError:
                # for empty data files, we have to manage the index_col differently
                df = pd.read_excel(f, na_values="-", index_col=0, skiprows=5, skipfooter=6)

            if df.empty:
                print("No data available in the above file.")
            else:
                date_cols = [datetime.strptime(c.replace("\n",' '), '%b \'%y').strftime('%Y-%m') for c in df.columns[1:]]
                # Rename columns because they originally are of format: "Jan\n'16", "Feb\n'16", etc.
                # We convert them into format like this: "2016-01", "2016-02", ...
                df.columns = [df.columns[0]] + date_cols
                df = df[date_cols] # then we drop any non-date columns (like 'TV Market Rnk' column)

                for market_name, row in df.iterrows():
                    for date, market_rating in row.items():
                        if not pd.isnull(market_rating): # only if it's not 'NaN'
                            short_name = mappings_df.loc[network_name, SHORT_NAME_COLUMN]
                            if not short_name in national_ratings_df.index:
                                # cases where short_name is not available or cannot be easily decided such as
                                # Azteca (Broadcast), for which we only have national rating for Azteca
                                # (not for broadcast specifically)
                                rating_indexes.append([network_name, market_name, short_name, date,
                                                       1.0, market_rating, 0.0])
                            else:
                                national_rating = national_ratings_df.loc[short_name, date]
                                if not pd.isnull(national_rating):
                                    rating_indexes.append([network_name, market_name, short_name, date,
                                                           market_rating / national_rating, market_rating,
                                                           national_rating])
                                else:
                                    # cases where we simply don't have ratings in national_ratings table (but the index exists)
                                    rating_indexes.append([network_name, market_name, short_name, date,
                                                           1.0, market_rating, 0.0])

        df = pd.DataFrame(rating_indexes, columns=["NetworkName", "MarketName", "NetworkCode", "Date",
                                                   "Index", "MarketRating", "NationalRating"])
        output_file = os.path.join(OUTPUT_FOLDER, output_file_name)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print("\nWrote index file at:", output_file)


if __name__ == '__main__':
    main()
    print("\nFinished calculating indexes for market monthly trend data.")
