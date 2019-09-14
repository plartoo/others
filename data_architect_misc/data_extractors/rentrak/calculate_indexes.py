"""
Author: Phyo Thiha
Last Modified: September 13, 2019
Description: This is to calculate DMA weights (indexes) for
individual networks (Market_Monthly_Trend), for each market based on
national ratings (Network_Monthly_Trend), both of which we have
downloaded using Selenium.
"""

import pdb

from datetime import datetime
import re
import csv
import os
import sys


import pandas as pd

INPUT_FOLDER = os.path.join(os.getcwd(), 'selenium_output')  # this is where selenium process dumps files
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'index_calculation_output')


def create_output_folder(output_folder):
    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


def get_network_name(file_path_and_name):
    # Extract network names from row#3 of RenTrak Market Monthly Trend Excel files
    df = pd.read_excel(file_path_and_name, nrows=1, skiprows=2)
    return df.columns[0].split(',')[0].strip()


def main():
    create_output_folder(OUTPUT_FOLDER)

    # # Step 1: Build national consolidated dataframe (clean ‘-‘, take out parens and put them as separate column)
    # # Select files which starts with 'Network_Monthly_Trend*' in the input folder
    # national_rating_files = [os.path.join(INPUT_FOLDER,f) for f in os.listdir(INPUT_FOLDER)
    #                          if (os.path.isfile(os.path.join(INPUT_FOLDER, f)) and 'Network_Monthly_Trend' in f)]
    #
    # dfs = []
    # for fi in national_rating_files:
    #     df = pd.read_excel(fi, na_values="-", index_col=0, skiprows=5, skipfooter=6)
    #     df.columns = [df.columns[0]] + [datetime.strptime(c.replace("\n",' '), '%b \'%y').strftime('%Y-%m') for c in df.columns[1:]]
    #     dfs.append(df)
    #
    # # Consolidate/merge all national ratings in one data frame
    # national_ratings_df = pd.concat(dfs, axis=1, sort=False)
    # national_ratings_df = national_ratings_df.groupby(national_ratings_df.columns, axis=1).first()#.fillna('')
    #
    # # Update network short names as indexes, and add original (full) network names as a new column.
    # # Short names are like 'ABCFAM' for 'ABC Family' because these codes are what we care in analysis and indexing
    # network_full_names = list(national_ratings_df.index)
    # network_short_names =  [re.findall(r'\((.*?)\)', n)[0] for n in network_full_names]
    # national_ratings_df.index = network_short_names
    # national_ratings_df.insert(0, "NetworkFullName", network_full_names, allow_duplicates=True)
    #
    # # Re-arrange columns so that NetworkFullName and Genre are the first ones (just because of my OCD)
    # date_cols = [c for c in national_ratings_df.columns if re.search(r'\d{4}\-\d{2}', c)]
    # non_date_cols = [c for c in national_ratings_df.columns if not re.search(r'\d{4}\-\d{2}', c)]
    # national_ratings_df = national_ratings_df[non_date_cols + date_cols]

    # national_ratings_df.to_csv('output.csv')
    # pdb.set_trace()
    # print('ha')

    network_rating_files = [os.path.join(INPUT_FOLDER,f) for f in os.listdir(INPUT_FOLDER)
                             if (os.path.isfile(os.path.join(INPUT_FOLDER, f)) and 'Market_Monthly_Trend' in f)]
    dfs = []
    for fi in network_rating_files:
        network_name = get_network_name(fi)
        df = pd.read_excel(fi, na_values="-", index_col=0, skiprows=5, skipfooter=6)
        df.columns = [df.columns[0]] + [datetime.strptime(c.replace("\n",' '), '%b \'%y').strftime('%Y-%m') for c in df.columns[1:]]
        dfs.append(df)


if __name__ == '__main__':
    main()
