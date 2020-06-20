"""
Script to join move-in data with parking waitlist.
"""

import pdb

import re

import pandas as pd

def main():
    waitlist_file = 'Parking_Waitlist_20191011_Cleaned.xlsx'
    move_in_file = 'Woodcliff_Move_In_Move_Out_Data_06122020_Cleaned.xlsx'
    dfw = pd.read_excel(waitlist_file)
    dfm = pd.read_excel(move_in_file)
    df = dfw.join(dfm.set_index('Unit'), on='Unit', rsuffix='_From_Move_In_Data')
    df.to_excel('Parking_Waitlist_20191011_Joined_With_Woodcliff_Move_In_Data_20200612.xlsx',
                index=False)
    print("Program completed.")


if __name__ == '__main__':
    main()

