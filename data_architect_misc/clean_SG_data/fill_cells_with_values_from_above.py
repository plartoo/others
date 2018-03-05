import pandas as pd
from datetime import date
import glob
import sys
import re

"""
Description:
Script to process Singapore raw data files.

Place this script in the folder where the raw Excel data files is. 
** MAKE SURE TO REMOVE ANY OTHER EXCEL FILES THAT ARE NOT MEANT TO BE PROCESSED.

Then, run as follow:
>> python fill_cells_with_values_from_above.py <pattern_of_the_file_names_to_process>
to process selected files that matches the pattern of the file names provided.

For example,
>> python fill_cells_with_values_from_above.py Spend_SG_Colgate_
will only process the Colgate (non-SOS) files in the folder and produce ONE final spend file.

Note: Python 3.5+ and pandas must be installed.
"""
# define parameters here; we can use optparse to cleanly feed as cmdline params later
rows_to_skip = 7 # will drop first non-null 8 rows in the raw file
rows_to_drop = [-1]
columns_to_drop = [0]
nonsos_column_names = ['Column2','Column3','Column4','Column5','Column6','Column7','$']
sos_column_names = ['Column2','Column3','Column4','Column5','Column6','$']
scrape_advertiser_after = r'SG_(.*?)_'
min_date = date.max # set to absolute max date possible; REF: https://stackoverflow.com/a/31972447
max_date = date.min

if len(sys.argv) > 1:
    file_name_pattern = '*' + sys.argv[1] + '*.xlsx'
else:
    print("\n******ATTENTION******")
    print("You must provide file name pattern as parameter to find the relevant input files in this folder.",
          "For example, try 'Spend_SG_' to process CP spend files and try 'Spend_SOS_SG_' for SOS file.")
    sys.exit()

files = glob.glob(file_name_pattern) # get all '.xlsx' files from the folder that matches the name pattern
final_df = pd.DataFrame()

for file_name in files:
    print("\nProcessing file: ", file_name)
    cur_df = pd.read_excel(file_name)
    cur_df.drop(cur_df.index[:rows_to_skip], inplace=True) # REF: https://goo.gl/8pKEAS and https://stackoverflow.com/a/17950081
    cur_df.drop(cur_df.index[rows_to_drop], inplace=True)
    cur_df.drop(cur_df.columns[columns_to_drop], axis=1, inplace=True) # REF: https://stackoverflow.com/a/18145399
    cur_df.fillna(method='ffill', inplace=True)# forward fill empty cells; REF: https://stackoverflow.com/a/27209766/1330974

    re_match =  re.search(scrape_advertiser_after, file_name, re.M|re.I)
    sos = re.search(r'SOS', file_name, re.M|re.I)
    if sos:
        cur_df.columns = sos_column_names # REF: https://stackoverflow.com/a/11346337
        cur_df.drop(cur_df[cur_df.Column6 == 'Total'].index, inplace=True)
        cur_df['Column6'] = cur_df['Column6'].apply(lambda x: x.date())
        min_date = min(cur_df['Column6']) if min_date > min(cur_df['Column6']) else  min_date
        max_date = max(cur_df['Column6']) if max_date < max(cur_df['Column6']) else  max_date 
        output_file_name = 'DS003g_Spend_SOS_SG'
    else:
        if re_match:
            advertiser = re_match.group(1)
            print("Advertiser: ", advertiser, "\n")
            cur_df.insert(loc=2, column='A', value=advertiser) # REF: https://stackoverflow.com/a/18674915
            cur_df.columns = nonsos_column_names
            cur_df['Column7'] = cur_df['Column7'].apply(lambda x: x.date())
            min_date = min(cur_df['Column7']) if min_date > min(cur_df['Column7']) else  min_date
            max_date = max(cur_df['Column7']) if max_date < max(cur_df['Column7']) else  max_date
            output_file_name = 'DS003g_Spend_SG'
            # print(cur_df)

    final_df = final_df.append(cur_df, ignore_index=True) # REF: https://stackoverflow.com/a/41529411

# write to excel
output_file_name += '_' + min_date.strftime('%Y%m') + 'to' + max_date.strftime('%Y%m') + '_Cleaned' + '.xlsx'
writer = pd.ExcelWriter(output_file_name)
final_df.to_excel(writer, 'Sheet1', index=False)
writer.save()

print('Output written to this file: ', output_file_name)
