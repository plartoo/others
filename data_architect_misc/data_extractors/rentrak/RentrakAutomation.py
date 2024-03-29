import re
import os
import glob
import numpy as np
import pdb
import pandas as pd
from datetime import datetime

def get_current_date():
    today = datetime.today()
    d1 = today.strftime("%Y%m%d")
    return d1


# Phyo: You can use pd.read_excel(f, na_values="-", index_col=1, skiprows=5, skipfooter=6) when loading the files
def fill_null_spaces(df):
    df = df.replace('-', '')
    return df

def replace_new_lines(df):
    df.columns = [x.replace('\n',' ') for x in df.columns.tolist()]
    return df

def concatfiles_vertically(a_l, m_z):
    frames = [a_l, m_z]
    result = pd.concat(frames)
    return result

def concatful_horizontally(frames):
    ##frames = [df1, df2, df3]
    # Phyo: Why reset the index?
    result = pd.concat(frames, sort=False).groupby(['Net', 'Genre']).first().reset_index()
    #result = result.groupby(['Net', 'Genre'])##.reset_index(drop=True)
    #result = df1.append(df2, ignore_index=True, sort=False)
    return result


def create_csv(combined_data):
    current_date = get_current_date()
    #print(combined_data)
    # Phyo: Use ''.join([str1, str2, ...]) https://stackoverflow.com/a/4166702
    export_csv = combined_data.to_csv(r'rentrak_report_automated' +
                        '_'+current_date+'.csv', sep='|')
    return export_csv

def main():
    dictionary = {}
    arr = []
    all_data=pd.DataFrame()
    # Phyo: this requires two nested for loops. We can do it with just one for loop (saving computation cost)
    for f in glob.glob("*A_L*.xlsx"):
        for i in glob.glob("*M_Z*.xlsx"):
            match1 = re.search('\d{4}\d{2}\d{2}', f) # date_pattern = '\d{8}'
            date1 = datetime.strptime(match1.group(), '%Y%m%d').date()
            match1 = re.search('\d{4}\d{2}\d{2}', i)
            date2 = datetime.strptime(match1.group(), '%Y%m%d').date()
            ##pdb.set_trace()  **Debug**
            if (date1 == date2):
                # Phyo: the names like 'dft1', 'dft2' etc. can be more explanatory/readable
                dft1 = pd.read_excel(f, header=5, skipfooter=6)
                dft2 = pd.read_excel(i, header=5, skipfooter=6)
                dfc1 = concatfiles_vertically(dft1, dft2)
                all_data.append(dfc1) # Phyo: where do we use all_data when we get out of 'for' loops?
                dictionary_concatenated = {f+' VS '+i:dfc1}
                dictionary.update(dictionary_concatenated) # Phyo: you can just do dictionary.update({f+' VS '+i:dfc1}), but even that, it doesn't tell me why we need a dictionary; I don't think we need it at all
                arr.append(dfc1)
                # Phyo: you can use 'import pdb' to check things on the fly instead of printing them for debugging.
                #print(dictionary)
                #print(date1)
                #print(date2)
                #print(f)
                #print(i)
                break;

    final_df = concatful_horizontally(arr)
    final_df = fill_null_spaces(final_df)
    final_df = replace_new_lines(final_df)
    print(final_df)
    create_csv(final_df)

main()