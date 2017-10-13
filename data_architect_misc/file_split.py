"""
Author: Phyo Thiha
Last Modified Date: Oct 13, 2017
Description:
Python helper library to split a given file in specified size.

Example Usage:
>> python file_split.py -f input.csv -s 10
OR
>> python file_split.py -f input.csv -s 10 -hr yes
OR
>> python file_split.py -f input.csv -s 10 -hr 1
OR for more info:
>> python file_split.py -h
"""

import argparse
import sys
import os.path
import csv
import pdb

def main():
    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(description='Split file into specified size (in MB).')
    parser.add_argument('-f', help='File name (including the full path if relevant. Example: "inputfile.csv"')
    parser.add_argument('-s'
                        , help='Desired size of each output (split) file in MB. '
                              'Example: "10" will split the original file into chunks each having 10MB'
                        , type=int)
    parser.add_argument('-hr'
                        , help='Include header row in each output file (default is y/1; also allows n/0 for "no"). '
                           'Example: "1" or "yes" will include header row from the original file in each output file.'
                        , default=1
                        , choices=['1','0','yes','no','y','n'])
    parser.add_argument('-o'
                        , help='Path of folder where the output files will be written. Example: "./output"'
                        , default=cur_dir_path)

    args = parser.parse_args()
    input_file = args.f
    file_size = args.s
    include_header = args.hr
    output_dir = args.o

    # if (!os.path.isfile(input_file)):
    #     print("Input file not found")
    #     sys.exit()
    #
    # if (os.path.splitext(input_file)[1] != 'csv'):
    #     print("Input file must be in CSV format")


    pdb.set_trace()
    print('Done')

if __name__ == "__main__":
    main()
