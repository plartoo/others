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

final_df = pd.DataFrame(columns=[
    'Advertiser', 'Brand', 'Product', 'AdCopy',
    'DurationInSecs', 'NetworkCode', 'Day', 'NationalTime',
    'L3AverageTelecastRatings', 'AverageTelecastAudience',
    'MarketName', 'Index', 'MarketWeightedTelecastRatings'])

for advertiser in df_l3.keys():
    # We will drop dupes, if any, because I have found in raw data file that there are usually duplicates
    cur_df_l3 = df_l3[advertiser].drop_duplicates()
    for df_l3_index, df_l3_row in cur_df_l3.iterrows():
        network_code = df_l3_row['Net']
        year_month = df_l3_row['Day'].strftime('%Y-%m')
        relevant_rating_index = df_index[(df_index['NetworkCode'] == network_code) & (df_index['Date'] == year_month)]
        for rating_index_index, rating_index_row in relevant_rating_index.iterrows():
            final_df = final_df.append(
                {'Advertiser': df_l3_row['Advertiser'],
                 'Brand': df_l3_row['Brand'],
                 'Product': df_l3_row['Product'],
                 'AdCopy': df_l3_row['Ad Copy'],
                 'DurationInSecs': df_l3_row['Duration (secs)'],
                 'NetworkCode': network_code,
                 'Day': df_l3_row['Day'],
                 'NationalTime': df_l3_row['National Time'],
                 'L3AverageTelecastRatings': df_l3_row['L+3 Avg Tlcst Rtg'],
                 'AverageTelecastAudience': df_l3_row['Avg Tlcst Aud'],
                 'MarketName': rating_index_row['MarketName'],
                 'Index': rating_index_row['Index'],
                 'MarketWeightedTelecastRatings': rating_index_row['Index'] * df_l3_row['L+3 Avg Tlcst Rtg'],
                 }, ignore_index=True)

pdb.set_trace()
print("Colpal weighted ratings written at:", output_file)

