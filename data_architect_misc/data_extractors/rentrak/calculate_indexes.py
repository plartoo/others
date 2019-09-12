"""
Author: Phyo Thiha
Last Modified: September 11, 2019
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


def main():
    create_output_folder(OUTPUT_FOLDER)

    # Step 1: Build national consolidated dataframe (clean ‘-‘, take out parens and put them as separate column)
    # Select files which starts with 'Network_Monthly_Trend*' in the input folder
    national_rating_files = [os.path.join(INPUT_FOLDER,f) for f in os.listdir(INPUT_FOLDER)
                             if (os.path.isfile(os.path.join(INPUT_FOLDER, f)) and 'Network_Monthly_Trend' in f)]
    # By sorting, we make it a bit easier for pandas concatenation
    # because now all columns will exist in the final data frame
    # before we start concatenating vertically across networks (say, from M-Z)
    national_rating_files.sort()

    final_df = pd.DataFrame()
    for fi in national_rating_files:
        df = pd.read_excel(fi, index_col=0, skiprows=5, skipfooter=6)
        # If there are networks that we have not seen, append them vertically in the final data frame
        if not(set(df.index).issubset(set(final_df.index))):
            print("\nintersect:", fi)
            df.columns = [df.columns[0]] + [datetime.strptime(c.replace("\n",' '), '%b \'%y').strftime('%Y-%m') for c in df.columns[1:]]
            # final_df = pd.concat([final_df, df[~df.index.isin(final_df.index)]]) # this is working
            final_df = final_df.append([df])
            # pdb.set_trace()
            # final_df.columns = [final_df.columns[0]] + [datetime.strptime(c.replace("\n",' '), '%b \'%y').strftime('%Y-%m') for c in final_df.columns[1:]]
            print('haa')
        else:
            print("\nno intersect:", fi)
            # pdb.set_trace()
            print('hee')
    final_df.to_csv('output.csv')
        #
    # df.loc[df.index[0],'Jan\n\'19']


if __name__ == '__main__':
    main()