"""
Script to generate a simple skeleton of JSON config file
that can be used as a base input for transform.py script.

Usage:
>> python generate_config.py

Running above command will output a new_config.json file.
User can modify (remove/add key-value pairs) as she needs
for her data transformation and then use it as follows:

>> python transform.py -c ./path/to/config/file/new_config.json

Author: Phyo Thiha
Last Modified: May 9, 2020
"""
import json
import os

from constants.transform_constants import *

CONFIG_TEMPLATE = [
    {
        f"__comment_for_input_file(s)__":
            f"(Required) If input file path and name are not provided as arguments via "
            f"commandline, enter the input folder and input file name (or the pattern of "
            f"input file names such as 'Russia_*.xlsx') to transform.",
        f"{KEY_INPUT_FOLDER_PATH}": "<example>./input/AED_Russia/",
        f"{KEY_INPUT_FILE_NAME_OR_PATTERN}": "<example>Russia_2019FY_20200402.xlsx",

        f"__comment_for_{PandasFileDataReader.KEY_ROWS_PER_READ}__":
            f"(Optional) The number of rows to read and transform per each iteration. "
            f"If the file has too many rows and if you have limited RAM on your machine, "
            f"you can enter a reasonable integer value below and "
            f"the data reader module will only process that many rows at a time "
            f"(thereby, preventing the out-of-memory errors). "
            f"Default rows that will be processed per iteration is shown below "
            f"and even if you don't define this key, the default value below will "
            f"be used by the program.",
        f"{PandasFileDataReader.KEY_ROWS_PER_READ}":
            PandasFileDataReader.KEY_ROWS_PER_READ,

        f"__comment_for_{PandasFileDataReader.KEY_KEEP_DEFAULT_NA}__":
            f"(Optional) By default, Pandas read empty cells as NaN. "
            f"We want to turn that off by default because in most of our "
            f"use cases, we want to leave empty cells as just empty. "
            f"For more detail, read 'keep_default_na' parameter from Pandas' "
            f"read_csv/read_excel methods. Note that if you leave this key "
            f"undefined, the default value will set be set to "
            f"{PandasFileDataReader.DEFAULT_KEEP_DEFAULT_NA} as shown below.",
        f"{PandasFileDataReader.KEY_KEEP_DEFAULT_NA}":
            PandasFileDataReader.DEFAULT_KEEP_DEFAULT_NA,

        f"__comment_for_{PandasFileDataReader.KEY_HEADER}__":
            f"(Optional) Enter the index of the row (note: in programming, "
            f"index starts from 0, so the first row in the data file would "
            f"have index=0) from which the program should read column headers from. "
            f"If column headers don't exist, do NOT define this key "
            f"(that is, delete this from the config file).",
        f"{PandasFileDataReader.KEY_HEADER}": PandasFileDataReader.DEFAULT_HEADER,

        f"__comment_for_{PandasFileDataReader.KEY_SKIP_ROWS}__":
            f"(Optional) Enter the index of the row (note: in programming, "
            f"index starts from 0, so the second row in the data file would "
            f"have index=1) where the data begins in the input file."
            f"In a typical input file, the data starts the second row "
            f"(the first row is the column headers), so the default value "
            f"for this key is set to '{PandasFileDataReader.DEFAULT_SKIP_ROWS}' "
            f"even if you don't define this key explicitly like below.",
        f"{PandasFileDataReader.KEY_SKIP_ROWS}": PandasFileDataReader.DEFAULT_SKIP_ROWS,

        f"__comment_for_{PandasFileDataReader.KEY_SKIP_FOOTER}__":
            f"(Optional) Enter the NUMBER of rows (note: not the index value), "
            f"which should be dropped from the bottom of the input file. "
            f"This can be used when input file has some footer rows "
            f"(such as Copyrights statement) that we want to drop. "
            f"But since it is not common to have footer rows, we set the "
            f"default for this key to {PandasFileDataReader.DEFAULT_SKIP_FOOTER} "
            f"even if you don't define this key explicitly like below.",
        f"{PandasFileDataReader.KEY_SKIP_FOOTER}":
            PandasFileDataReader.DEFAULT_SKIP_FOOTER,

        f"__comment_for_{PandasExcelDataReader.KEY_SHEET_NAME}__":
            f"(Optional) If your input file(s) is/are Excel, you can define "
            f"the sheet name to read/process. If you leave this key undefined, "
            f"the program will read first sheet, with index "
            f"{PandasExcelDataReader.DEFAULT_SHEET_TO_READ} by default. "
            f"You can also leave this key undefined if your input file is not "
            f"a CSV file or if you are okay with the default value below.",
        f"{PandasExcelDataReader.KEY_SHEET_NAME}":
            PandasExcelDataReader.DEFAULT_SHEET_TO_READ,

        f"__comment_for_{PandasCSVDataReader.KEY_INPUT_CSV_DELIMITER}__":
            f"(Optional) If your input file(s) is/are CSV, you can define "
            f"the delimiter used in that input file. If you leave this key undefined, "
            f"the program will use the default delimiter value as "
            f"'{PandasCSVDataReader.KEY_INPUT_CSV_DELIMITER}'. "
            f"You can also leave this key undefined if your input file is not "
            f"a CSV file or if you are okay with the default value below.",
        f"{PandasCSVDataReader.KEY_INPUT_CSV_DELIMITER}":
            f"{PandasCSVDataReader.KEY_INPUT_CSV_DELIMITER}",

        f"__comment_for_{PandasCSVDataReader.KEY_INPUT_FILE_ENCODING}__":
            f"(Optional) If your input file(s) is/are CSV, you can define "
            f"the encoding used in that input file. If you leave this key undefined, "
            f"the program will use the default encoding value as None, which "
            f"will be interpreted as 'utf-8' encoding by Pandas."
            f"You can also leave this key undefined if your input file is not "
            f"a CSV file or if you are okay with the default value below.",
        f"{PandasCSVDataReader.KEY_INPUT_FILE_ENCODING}": 'utf-8',

        f"__comment_for_{PandasCSVDataReader.KEY_SKIP_BLANK_LINES}__":
            f"(Optional) If your input file(s) is/are CSV, you can define "
            f"if blank lines will be skipped in reading the input file. "
            f"By default, the program will NOT skip the blank lines "
            f"(meaning, the value will still be set to "
            f"{PandasCSVDataReader.DEFAULT_SKIP_BLANK_LINES}) even if you "
            f"leave this key undefined.",
        f"{PandasCSVDataReader.KEY_SKIP_BLANK_LINES}":
            PandasCSVDataReader.DEFAULT_SKIP_BLANK_LINES,

        f"__comment_for_output_file(s)__":
            f"(Optional) The key below, '{KEY_WRITE_OUTPUT}', can be used "
            f"to decide if the processed data will be written to an output "
            f"destination (a file or a SQL table). The default is as shown "
            f"below and it will be used even if you leave this key undefined.",
        f"{KEY_WRITE_OUTPUT}": DEFAULT_WRITE_OUTPUT,

        f"__comment_for_{KEY_DATA_WRITER_MODULE_FILE}__":
            f"(Optional) The key below, '{KEY_DATA_WRITER_MODULE_FILE}', "
            f"can be used to specify which data writer module (such as "
            f"Excel, CSV or SQL) will be used to write the processed data. "
            f"The default value is as shown below and it will be used even if you "
            f"leave this key undefined.",
        f"{KEY_DATA_WRITER_MODULE_FILE}": f"{DEFAULT_DATA_WRITER_MODULE_FILE}",

        f"__comment_for_{FileDataWriter.KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE}__":
            f"(Optional) The key below can be used to specify if index column from "
            f"Pandas dataframe should be included in the output file. "
            f"The default value is as shown below and it will be used even if you "
            f"leave this key undefined.",
        f"{FileDataWriter.KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE}":
            FileDataWriter.DEFAULT_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE,

        f"__comment_for_{FileDataWriter.KEY_OUTPUT_FOLDER_PATH}__":
            f"(Optional) The key below can be used to specify where the "
            f"processed data will be written."
            f"The default value is as shown below and it will be used "
            f"even if the key below is undefined.",
        f"{FileDataWriter.KEY_OUTPUT_FOLDER_PATH}":
            f"{FileDataWriter.DEFAULT_OUTPUT_FOLDER_PATH}",

        f"__comment_for_{FileDataWriter.KEY_OUTPUT_FILE_PREFIX}__":
            f"(Optional) The key below can be used to specify the beginning "
            f"part (prefix) of the output file name (e.g., 'prefix_*.xlsx'). "
            f"The default value is None (empty string) and it will be used "
            f"even if the key below is undefined.",
        f"{FileDataWriter.KEY_OUTPUT_FILE_PREFIX}": '',

        f"__comment_for_{FileDataWriter.KEY_OUTPUT_FILE_SUFFIX}__":
            f"(Optional) The key below can be used to specify the last "
            f"part (suffix) of the output file name (e.g., '*_suffix.xlsx'). "
            f"The default value is None (empty string) and it will be used "
            f"even if the key below is undefined.",
        f"{FileDataWriter.KEY_OUTPUT_FILE_SUFFIX}": '',

        f"__comment_for_{FileDataWriter.KEY_OUTPUT_FILE_ENCODING}__":
            f"(Optional) The key below can be used to specify the encoding "
            f"of the output file. For options available standard encoding "
            f"in Python, please see: "
            f"https://docs.python.org/3/library/codecs.html. "
            f"The default value is None (which is interpreted by Pandas as "
            f"'utf-8', and it will be used even if the key below is undefined.",
        f"{FileDataWriter.KEY_OUTPUT_FILE_ENCODING}": 'utf-8',

        f"__comment_for_{ExcelDataWriter.KEY_OUTPUT_SHEET_NAME}__":
            f"(Optional) If your output file is Excel, you can define "
            f"the sheet name to write the data to. "
            f"The program will write to the default sheet name as shown below "
            f"even if the key is not defined.",
        f"{ExcelDataWriter.KEY_OUTPUT_SHEET_NAME}":
            f"{ExcelDataWriter.DEFAULT_OUTPUT_SHEET_NAME}",

        f"__comment_for_{CSVDataWriter.KEY_OUTPUT_DELIMITER}__":
            f"(Optional) If your output file is CSV, you can define "
            f"the delimiter to use in the output file. "
            f"The program will use the default delimiter as shown below "
            f"even if the key is not defined.",
        f"{CSVDataWriter.KEY_OUTPUT_DELIMITER}":
            f"{CSVDataWriter.DEFAULT_OUTPUT_DELIMITER}",

        f"__comment_for_{MSSQLDataWriter.KEY_DATABASE_SCHEMA}__":
            f"(Required if you want to write your data to MS SQL table) "
            f"Use this key to define the scheme to write the data to. "
            f"If you instruct the program to write to SQL table and "
            f"don't define the key below, the program will raise an "
            f"error letting you know.",
        f"{MSSQLDataWriter.KEY_DATABASE_SCHEMA}": None,

        f"__comment_for_{MSSQLDataWriter.KEY_DATABASE_SCHEMA}__":
            f"(Optional) If you want to write output data to MS SQL table, "
            f"use the key below to define the destination table name. "
            f"If the key is not defined, the default value as shown below "
            f"will be used.",
        f"{MSSQLDataWriter.KEY_OUTPUT_TABLE_NAME}":
            f"{MSSQLDataWriter.DEFAULT_OUTPUT_TABLE_NAME}",

        f"__comment_for_{MSSQLDataWriter.KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE}__":
            f"(Optional) If you want to write the index of output dataframe "
            f"to MS SQL table, use the key below. "
            f"If the key is not defined, the default value as shown below "
            f"will be used.",
        f"{MSSQLDataWriter.KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE}":
            MSSQLDataWriter.DEFAULT_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE,

        f"__comment_for_{KEY_CUSTOM_TRANSFORM_FUNCTIONS_FILE}__":
            f"(Optional) Path+name of the file that has *CUSTOM* data transformation "
            f"functions, which will be imported and used in the data processing tasks. "
            f"Default value is as shown below and it will be used even if this key is "
            f"not defined.",
        f"{KEY_CUSTOM_TRANSFORM_FUNCTIONS_FILE}":
            f"{DEFAULT_COMMON_TRANSFORM_FUNCTIONS_FILE}",

        f"__comment_for_{KEY_FUNCTIONS_TO_APPLY}__":
            "(Required) List of functions and parameters to be used in data processing. "
            "These functions must be defined in the transform function/module file, "
            "which is defined with the key 'KEY_CUSTOM_TRANSFORM_FUNCTIONS_FILE' above.",
        f"{KEY_FUNCTIONS_TO_APPLY}":
            [
                {
                    f"__function_comment__": f"Data files sometimes have empty columns. We need to drop them first.",
                    f"{KEY_FUNC_NAME}": "drop_unnamed_columns"
                },
                {
                    f"__function_comment__": f"By the time we run this function, there should be "
                                             f"only 13 columns total remaining in the raw dataframe.",
                    f"{KEY_FUNC_NAME}": "assert_number_of_columns_equals",
                    f"{KEY_FUNC_ARGS}": [13]
                },
            ]
    }
]


def main():
    json_file = os.path.join(os.getcwd(),'config_template.json')
    print(f"Generated skeleton JSON config file with all valid keys to => "
          f"{json_file}")
    with open(json_file, 'w') as out_file:
        json.dump(CONFIG_TEMPLATE, out_file, indent=4)


if __name__ == '__main__':
    main()
