import os
import re
import glob
import csv

"""
Draft code to translate numerical values into qualitative ratings and labels in survey data using a mapping file.

Here,
"""


key = 'HOUSING RECORD' # another key to process is: 'PERSON RECORD'
input_folder_name = '' # make sure this folder is in the same folder as this Python script
output_folder_name = 'processed'
input_folder_path = os.path.dirname(os.path.realpath(__file__))
input_folder = os.path.join(input_folder_path, input_folder_name)
input_files = glob.glob(input_folder + '/*.csv')

mapping_file = os.path.join('mappings', 'mappings.csv') # TODO: update this to be more general

# Build mapping dictionary from the mapping/lookup file
with open(mapping_file, 'r') as incsv:
    csvreader = csv.reader(incsv)
    row_cnt = 0
    mappings = {}
    for row in csvreader:
        row_cnt += 1
        if row_cnt == 1:
            pass
        else:
            record_type = row[0]
            var_name = row[1]
            var_codes_1 = row[5]
            var_codes_2 = row[6]

            if record_type in mappings:
                if var_name in mappings[record_type]:
                    if var_codes_1 in mappings[record_type][var_name]:
                        mappings[record_type][var_name][var_codes_1] = var_codes_2 # overwrite the existing value
                    else:
                        mappings[record_type][var_name][var_codes_1] = var_codes_2

                else:
                    mappings[record_type][var_name] = {}
                    mappings[record_type][var_name][var_codes_1] = var_codes_2
            else:
                mappings[record_type] = {}
                mappings[record_type][var_name] = {}
                mappings[record_type][var_name][var_codes_1] = {}
                mappings[record_type][var_name][var_codes_1] = var_codes_2

output_folder = os.path.join(input_folder_path, output_folder_name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_file_name = 'housing_record_mreged.csv' # TODO: make this general
output_file = os.path.join(output_folder, output_file_name)

header_recorded = False

with open(output_file, 'w',  newline='') as outcsv:
    csvwriter = csv.writer(outcsv)

    for f in input_files:
        state = re.search('(.{2}).csv', f).group(1)

        with open(f, 'r') as incsv:
            csvreader = csv.reader(incsv)
            row_cnt = 0
            for row in csvreader:
                row_cnt += 1
                if row_cnt == 1:
                    if not header_recorded:
                        row.append('state') # TODO: remove this to make it general
                        header = row
                        csvwriter.writerow(header)
                        header_recorded = True
                else:
                    row.append(state)
                    for i,r in enumerate(row):
                        orig_val = r
                        col_name = header[i]
                        if (col_name in mappings[key]) and (r in mappings[key][col_name]):
                            val_to_translate = mappings[key][col_name][r]
                        else:
                            val_to_translate = orig_val

                        row[i] = val_to_translate
                    csvwriter.writerow(row)

print('Translating survey data finished')