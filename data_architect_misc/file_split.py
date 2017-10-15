"""
Author: Phyo Thiha
Last Modified Date: Oct 13, 2017
Description:
Python helper library to split a given file in specified size.
The output files will be written in a folder named after the input file in the directory where this code lives.

Note: We assume the CSV files are in utf-8 encoding.
We also assume the first row in input file is the header row.

Example Usage:
>> python file_split.py -f input.csv -s 10
OR
>> python file_split.py -f input.csv -s 10 -hr y
OR
>> python file_split.py -f input.csv -s 10 -hr 1
OR for more info:
>> python file_split.py -h
"""

import argparse
import sys
import os.path
import csv


def get_size_in_bytes(str, encoding):
    # Ref1: https://stackoverflow.com/a/4013418
    # Ref2: https://stackoverflow.com/q/5290182
    return len(str.encode(encoding))


def main():
    ENCODING = 'utf-8'
    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(description='Split file into specified size (in MB).')
    parser.add_argument('-f', help='File name (including the full path if relevant). '
                                   'Example: "C:\path\to\inputfile.csv"')
    parser.add_argument('-s'
                        , help='Desired size of each output (split) file in MB. '
                              'Example: "10" will split the original file into chunks each having 10MB'
                        , type=int)
    parser.add_argument('-hr'
                        , help='(Optional) Include header row in each output file (default is y/1; also allows n/0 '
                               'for "no"). Example: "1" or "y" will include header row from the original file in '
                               'each output file. Otherwise, only the first output file will have header row.'
                        , default=1
                        , choices=['1','0','y','n'])

    args = parser.parse_args()
    if not args.s:
        sys.exit('Run "> python file_split.py -h" to learn how to use this program')
    input_file = args.f
    # We'll use decimal-based unit for MB to bytes conversion: https://www.google.com/search?q=How+many+MB+are+in+1+GB
    file_size_limit = abs(args.s) * 1000 * 1000
    include_header = args.hr

    input_file_basename = os.path.splitext(input_file)[0] # without extension such as '.csv'
    output_folder = os.path.join(cur_dir_path, input_file_basename)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_file, newline='', encoding=ENCODING) as fi:
        reader = csv.reader(fi)

        try:
            row_cnt = 0
            header_row_size = 0
            cur_doc_size = 0
            file_cnt = 0
            header = []
            cur_doc = []
            for row in reader:
                row_cnt += 1
                cur_row_size = get_size_in_bytes(','.join(row), ENCODING)

                if row_cnt == 1:
                    header = row
                    if (include_header in ['1', 'y']):
                        header_row_size = get_size_in_bytes(','.join(header), ENCODING)
                        cur_doc.append(header)
                        cur_doc_size += header_row_size
                else:
                    if (cur_doc_size + cur_row_size) <= file_size_limit:
                        cur_doc.append(row)
                        cur_doc_size += cur_row_size
                    else:
                        output_file_name = ''.join([input_file_basename, '_', str(file_cnt), '.csv'])
                        output_file = os.path.join(output_folder, output_file_name)
                        with open(output_file, 'w', newline='', encoding=ENCODING) as fo:
                            try:
                                writer = csv.writer(fo)
                                writer.writerows(cur_doc)
                                file_cnt += 1
                                print('Wrote file: ', output_file, '\t\tof size: ', cur_doc_size,
                                      '\t\thaving row count: ', len(cur_doc), '\n')
                            except csv.Error as e:
                                print('Error in writing an output CSV file: ', output_file_name)
                                sys.exit()

                        cur_doc = []
                        if (include_header in ['1', 'y']):
                            cur_doc.append(header)
                            cur_doc_size = header_row_size
                        cur_doc.append(row)
                        cur_doc_size += cur_row_size

            output_file_name = ''.join([input_file_basename, '_', str(file_cnt), '.csv'])
            output_file = os.path.join(output_folder, output_file_name)
            with open(output_file, 'w', newline='', encoding=ENCODING) as fo:
                try:
                    writer = csv.writer(fo)
                    writer.writerows(cur_doc)
                    file_cnt += 1
                    print('Wrote file: ', output_file, '\t\tof size: ', cur_doc_size,
                          '\t\thaving row count: ', len(cur_doc), '\n')
                except csv.Error as e:
                    print('Error in writing an output CSV file: ', output_file_name)
                    sys.exit()

        except csv.Error as e:
            print('Error in reading input CSV file. Make sure the full path to input file is correct.')
            sys.exit('file {}, line {}: {}'.format(input_file, reader.line_num, e))

    print('\nSplitting file successfully done for: ', input_file)


if __name__ == "__main__":
    main()
