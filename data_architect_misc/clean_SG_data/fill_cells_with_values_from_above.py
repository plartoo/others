import pandas as pd
import os.path
import glob
import sys

"""
Description:
Script to process Singapore raw data files.

Place this script in the folder where the raw Excel data files is. 
** MAKE SURE TO REMOVE ANY OTHER FILES THAT ARE NOT MEANT TO BE PROCESSED.

Then, run as follow:
>> python fill_cells_with_values_from_above.py 
to process ALL Excel files in the folder and merge them into one. OR

>> python fill_cells_with_values_from_above.py <pattern_of_the_file_names_to_process>
to process selected files that matches the pattern of the file names provided.

For example,
>> python fill_cells_with_values_from_above.py Spend_SG_Colgate_
will only process the Colgate (non-SOS) files in the folder and produce ONE final spend file.

Note: Python 3.5+ and pandas must be installed.
"""
# define parameters here; we can turn them into args to be fed as cmdline arguments later
rows_to_skip = 7 # will drop first non-null 8 rows in the raw file
rows_to_drop = [-1]
columns_to_drop = [0]
new_column_names = ['Category','Subcategory','Product','Media','Period','Spend']
output_file_name = 'processed.xlsx'

if os.path.isfile(output_file_name):
    print("\n******ATTENTION******")
    print("Output file named ''", output_file_name ,"'' already exists in the folder. "
                                                 "Please remove/rename that first and rerun the code.")
    sys.exit()

if len(sys.argv) > 1:
    file_name_pattern = '*' + sys.argv[1] + '*.xlsx'
else:
    file_name_pattern = '*.xlsx'

files = glob.glob(file_name_pattern) # get all '.xlsx' files from the folder that matches the name pattern
final_df = pd.DataFrame()

for file_name in files:
    print(file_name)
    cur_df = pd.read_excel(file_name)
    cur_df.drop(cur_df.index[:rows_to_skip], inplace=True) # REF: https://goo.gl/8pKEAS and https://stackoverflow.com/a/17950081
    cur_df.drop(cur_df.index[rows_to_drop], inplace=True)
    cur_df.drop(cur_df.columns[columns_to_drop], axis=1, inplace=True) # REF: https://stackoverflow.com/a/18145399
    cur_df.fillna(method='ffill', inplace=True)# forward fill empty cells; REF: https://stackoverflow.com/a/27209766/1330974
    cur_df.columns = new_column_names # REF: https://stackoverflow.com/a/11346337
    print(cur_df)
    final_df = final_df.append(cur_df, ignore_index=True) # REF: https://stackoverflow.com/a/41529411

# write to excel
writer = pd.ExcelWriter(output_file_name)
final_df.to_excel(writer, 'Sheet1', index=False)
writer.save()

print('Output written to this file: ', output_file_name)
