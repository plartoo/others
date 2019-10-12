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

dfl = pd.read_excel(l3_rating_file, sheet_name=l3_rating_sheets,
                    usecols = ['Advertiser', 'Brand', 'Product', 'Ad Copy', 'Duration (secs)',
                               'Net', 'Day', 'National Time', # market name, market-weighted telecast ratings
                               'L+3 Avg Tlcst Rtg', 'Avg Tlcst Aud'],
                    skiprows=6, skipfooter=7)

dfi = pd.read_csv(index_file)

min_date = min([dfl[k]['Day'].min() for k in dfl.keys()]).strftime('%Y-%m')
max_date = max([dfl[k]['Day'].max() for k in dfl.keys()]).strftime('%Y-%m')
print("Selecting index data between these date ranges (they are usually the same):", min_date, "and", max_date)
dfi = dfi[(dfi['Date'] >= min_date) & (dfi['Date'] <= max_date)]
pdb.set_trace()
print("Colpal weighted ratings written at:", output_file)

