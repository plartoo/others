"""
Script to extract resident move-in dates from raw data file.
"""

import re

import pandas as pd

def reset_extracted_row():
    return {
        'Unit': '',
        'Name': '',
        'Move_in_Date': '',
        'Total': 0
    }


def main():
    waitlist_file = 'Parking_Waitlist_20191011_Cleaned.xlsx'

    move_in_file = 'Woodcliff_Move_In_Move_Out_Data_06122020.xlsx'
    sheets = pd.read_excel(move_in_file, sheet_name=None)
    extracted_data = []
    for name, sheet in sheets.items():
        print(f"Processing sheet: {name}")
        df = sheet
        df1 = df[['Unit', 'Resident', 'Move In', 'Unnamed: 9', 'Unnamed: 10']] # select only columns of interest
        df1 = df1.drop(df.index[0]) # drop second header row
        extracted_row = reset_extracted_row()
        for index, row in df1.iterrows():
            if re.match(r'.*Blvd.*', str(row.Unit), re.I|re.M):
                # print(row.Unit)
                extracted_row['Unit'] = '-'.join(re.search(r'(\d+).?Blvd.*?#(.*?)$', row.Unit).groups())
            if not pd.isna(row.Resident):
                extracted_row['Name'] = row.Resident
            if not pd.isna(row['Move In']):
                extracted_row['Move_in_Date'] = row['Move In']
            if row['Unnamed: 9'] == 'Total':
                extracted_row['Total'] = row['Unnamed: 10']
                extracted_data.append(extracted_row)
                extracted_row = reset_extracted_row()

    df_extracted = pd.DataFrame(extracted_data)
    move_in_file_processed = move_in_file.split('.')
    move_in_file_processed.insert(1, '_processed')
    move_in_file_processed.insert(2, '.')
    df_extracted.to_excel(''.join(move_in_file_processed), index=False)
    print("Program completed.")


if __name__ == '__main__':
    main()

