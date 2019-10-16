"""
Author: Phyo Thiha
Last Modified: October 11, 2019
Description: This is to calculate market-based (weighted) ratings for
Colgate and its competitors' RenTrak national ratings.

Usage:
>> python calculate_colpal_ratings.py -i1 toothpaste_ratings.xlsx
-i2 .\index_calculation_output\rating_indexes_20190101_20191001.csv
-s Colgate Crest Sensodyne -o l3_weighted_ratings.csv

IMPORTANT NOTE: Before running this script, we must create a index
file using Market Monthly Trend and Network Monthly Trend
files. Use 'calculate_indexes.py' script to generate that file, and
ONLY AFTER THAT, run this script.
"""

# python calculate_colpal_ratings.py -i1 toothpaste_ratings.xlsx -i2 .\index_calculation_output\rating_indexes_20190101_20191001.csv -s Colgate Crest Sensodyne -o l3_weighted_ratings.csv
import pdb

import argparse
from collections import defaultdict
from datetime import datetime
import re
import os
import sys

import pandas as pd

parser = argparse.ArgumentParser(description='Calculate market-based (weighted) ratings for Colgate '
                                             'and its competitors using indexes built on Rentrak national '
                                             'and market ratings.')
parser.add_argument('-i1', required=True, type=str,
                    help='Excel file that has L+3 ratings for Colpal and its competitor products.')
parser.add_argument('-s', nargs='+', required=True,
                    help='Sheet names to be used from Excel file with L+3 ratings.')
parser.add_argument('-i2', required=True, type=str,
                    help='CSV file that has rating indexes calculated by "calculate_indexes.py" script.')
parser.add_argument('-o', required=True, type=str,
                    help='Output file for calculation results.')
args = parser.parse_args()

l3_rating_file = args.i1
l3_rating_sheets = args.s
index_file = args.i2
output_file = args.o

df_l3 = pd.read_excel(l3_rating_file, sheet_name=l3_rating_sheets,
                      usecols = ['Advertiser', 'Brand', 'Product', 'Ad Copy', 'Duration (secs)',
                               'Net', 'Day', 'National Time', # market name, market-weighted telecast ratings
                               'L+3 Avg Tlcst Rtg', 'Avg Tlcst Aud'],
                      skiprows=6, skipfooter=7)
df_index = pd.read_csv(index_file)

min_date = min([df_l3[k]['Day'].min() for k in df_l3.keys()]).strftime('%Y-%m')
max_date = max([df_l3[k]['Day'].max() for k in df_l3.keys()]).strftime('%Y-%m')
print("Selecting index data between these date ranges (they are usually the same):", min_date, "and", max_date)
df_index = df_index[(df_index['Date'] >= min_date) & (df_index['Date'] <= max_date)]

final_df_dict = defaultdict(list)
for advertiser in df_l3.keys():
    # We will drop dupes, if any, because I have found in raw data file that there are usually duplicates
    cur_df_l3 = df_l3[advertiser].drop_duplicates()
    for df_l3_index, df_l3_row in cur_df_l3.iterrows():
        print("\n", df_l3_row)
        network_code = df_l3_row['Net']
        year_month = df_l3_row['Day'].strftime('%Y-%m')
        relevant_rating_index_df = df_index[(df_index['NetworkCode'] == network_code) & (df_index['Date'] == year_month)]
        for rating_index_index, rating_index_row in relevant_rating_index_df.iterrows():
            final_df_dict['Advertiser'].append(df_l3_row['Advertiser'])
            final_df_dict['Brand'].append(df_l3_row['Brand'])
            final_df_dict['Product'].append(df_l3_row['Product'])
            final_df_dict['AdCopy'].append(df_l3_row['Ad Copy'])
            final_df_dict['DurationInSecs'].append(df_l3_row['Duration (secs)'])
            final_df_dict['NetworkCode'].append(network_code)
            final_df_dict['Day'].append(df_l3_row['Day'])
            final_df_dict['NationalTime'].append(df_l3_row['National Time'])
            final_df_dict['L3AverageTelecastRatings'].append(df_l3_row['L+3 Avg Tlcst Rtg'])
            final_df_dict['AverageTelecastAudience'].append(df_l3_row['Avg Tlcst Aud'])
            final_df_dict['MarketName'].append(rating_index_row['MarketName'])
            final_df_dict['Index'].append(rating_index_row['Index'])
            final_df_dict['MarketWeightedTelecastRatings'].append(rating_index_row['Index'] * df_l3_row['L+3 Avg Tlcst Rtg'])

df_final = pd.DataFrame.from_dict(final_df_dict)
df_final.to_csv(output_file)
print("Colpal weighted ratings written at:", output_file)
