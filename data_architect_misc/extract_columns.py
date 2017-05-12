import os
import glob
import csv

desired_cols = [    # provide list of columns that you'd like to extract from the input files
    'WAVE',
    'DUMINTERVWID',
    'DUMENDDATE',
    'QB10GRID_1',
    'QB30GRID_1_3',
    'QB30GRID_1_8',
    'QB30GRID_1_12',
    'QB30GRID_1_15',
    'QB30GRID_1_16',
    'QB40GRID_1_01',
    'QB40GRID_1_02',
    'QB40GRID_1_03',
    'QB40GRID_1_04',
    'QB40GRID_1_06',
    'QB40GRID_1_10',
    'QB40GRID_1_11',
    'QB40GRID_1_12',
    'QB40GRID_1_13',
    'QB40GRID_1_14',
    'QB40GRID_1_18',
    'QB40GRID_1_19',
    'OQP30_TOTAL_FINAL_1',
    'QP10_QP20_FINAL_1'
]

input_folder_name = 'BrandHealth' # make sure this folder is in the same folder as this Python script
output_folder_name = input_folder_name + '_Extracted'
input_folder_path = os.path.dirname(os.path.realpath(__file__))
input_folder = os.path.join(input_folder_path, input_folder_name)
#input_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
input_files = glob.glob(input_folder + '/*')

output_folder = os.path.join(input_folder_path, output_folder_name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for f in input_files:
    output_data = [desired_cols]
    output_file_name = os.path.splitext(os.path.basename(f))[0] + '_Extracted.csv'
    output_file = os.path.join(output_folder, output_file_name)

    with open(f, 'r') as incsv:
        csvreader = csv.reader(incsv)
        row_cnt = 0
        for row in csvreader:
            output_row = []
            row_cnt += 1
            if row_cnt == 1:
                col_idx = {x:i for i,x in enumerate(row)}
            else:
                for c in desired_cols:
                    if c in col_idx:
                        try:
                            output_row.append(row[col_idx[c]])
                        except IndexError as e:
                            print(f)
                            print(row)
                            print(row_cnt, ': ', col_idx[c])
                    else:
                        output_row.append('')
                output_data.append(output_row)

        with open(output_file, 'w',  newline='') as outcsv:
            csvwriter = csv.writer(outcsv)
            csvwriter.writerows(output_data)

print('ha')