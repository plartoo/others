import pdb

import importlib
import json
import pandas as pd
import pathlib
import os
import sys

import transform_errors

# TODO 1: in 'read_data' function it seems silly to have to check
# is_excel/is_csv and retrieve relevant parameters (like delimiter)
# every time we read. Let's create a class (say, 'DataReader') and
# do it the OOP way.
# TODO 2: write generate_config_json function
# TODO 3: document methods (use pydoc to generate documentation?)
# TODO 4: (maybe) unit tests
# TODO 5: (maybe) explore if we can pass other params such as
# quotechar; quoting; doublequote; escapechar etc. via kwargs.
# Tangential REF for read by chunk in Pandas:
# https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#iterating-through-files-chunk-by-chunk
# Other useful REFs:
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
# https://cmdlinetips.com/2018/04/how-to-drop-one-or-more-columns-in-pandas-dataframe/
# https://jeffdelaney.me/blog/useful-snippets-in-pandas/
# https://www.giacomodebidda.com/reading-large-excel-files-with-pandas/

# Constants for config file
KEY_INPUT_FOLDER_PATH = 'input_folder_path'
KEY_INPUT_FILE_NAME_OR_PATTERN = 'input_file_name_or_pattern'
KEY_OUTPUT_FOLDER_PATH = 'output_folder_path'
KEY_OUTPUT_FILE_PREFIX = 'output_file_name_prefix'
KEY_TRANSFORM_FUNCTIONS_FILE = 'transform_functions_file'
# We will assume the transform_functions.py file is: './transform_functions/transform_functions.py'
VALUE_TRANSFORM_FUNCTIONS_FILES_DEFAULT = os.path.join(os.getcwd(), 'transform_functions', 'transform_functions.py')

KEY_SHEET_NAME = 'sheet_name_of_excel_file'
VALUE_SHEET_NAME_DEFAULT = 'Sheet1'

KEY_ROW_INDEX_OF_COLUMN_HEADERS = 'row_index_to_extract_column_headers'
VALUE_COLUMN_HEADER_ROW_NUM_DEFAULT = -1

# Note: we tested and found that pandas' csv sniffer isn't very good
# (even when using 'Python' as parser engine) in detecting delimiters, so
# setting this as None is not good enough. Thus we decided to set the default
# for 'VALUE_INPUT_CSV_DELIMITER_DEFAULT' as comma.
KEY_INPUT_CSV_ENCODING = 'input_csv_file_encoding'
VALUE_INPUT_CSV_ENCODING_DEFAULT = None # None defaults to 'utf-8' in pandas
KEY_INPUT_CSV_DELIMITER = 'input_csv_file_delimiter'
VALUE_INPUT_CSV_DELIMITER_DEFAULT = ','
KEY_OUTPUT_CSV_ENCODING = 'output_csv_file_encoding'
VALUE_OUTPUT_CSV_ENCODING_DEFAULT = None # None defaults to 'utf-8' in pandas
KEY_OUTPUT_CSV_DELIMITER = 'output_csv_file_delimiter'
VALUE_OUTPUT_CSV_DELIMITER_DEFAULT = '|'

KEY_ROW_INDEX_WHERE_DATA_STARTS = 'row_index_where_data_starts'
VALUE_ROW_INDEX_WHERE_DATA_STARTS_DEFAULT = 1
KEY_BOTTOM_ROWS_TO_SKIP = 'num_of_rows_to_skip_from_the_bottom'
VALUE_BOTTOM_ROWS_TO_SKIP_DEFAULT = 0

KEY_ROWS_PER_CHUNK_FOR_CSV = 'rows_per_chunk_for_csv'
VALUE_ROWS_PER_CHUNK_FOR_CSV_DEFAULT = 1500000

# Keys in config file and their expected data types
EXPECTED_CONFIG_DATA_TYPES = {
    KEY_INPUT_FOLDER_PATH: [str],
    KEY_INPUT_FILE_NAME_OR_PATTERN: [str],
    KEY_OUTPUT_FOLDER_PATH: [str],
    KEY_OUTPUT_FILE_PREFIX: [str],
    KEY_SHEET_NAME: [str],

    KEY_INPUT_CSV_ENCODING: [str],
    KEY_INPUT_CSV_DELIMITER: [str],
    KEY_OUTPUT_CSV_ENCODING: [str],
    KEY_OUTPUT_CSV_DELIMITER: [str],
    KEY_ROW_INDEX_OF_COLUMN_HEADERS: [int],
    KEY_ROW_INDEX_WHERE_DATA_STARTS: [int],
    KEY_BOTTOM_ROWS_TO_SKIP: [int],
    KEY_ROWS_PER_CHUNK_FOR_CSV: [int],
}

# Keys in config file that must exist (required keys)
REQUIRED_KEYS = [KEY_INPUT_FOLDER_PATH,
                 KEY_INPUT_FILE_NAME_OR_PATTERN,
                 KEY_OUTPUT_FOLDER_PATH]

# Other constants
CSV_FILE_EXTENSION = '.csv'
EXCEL_FILE_EXTENSION_OLD = '.xls'
EXCEL_FILE_EXTENSION_NEW = '.xlsx'

DESC = """This program transform raw data files according to the procedures 
and rules defined in the JSON configuration file (e.g., config.json), 
which must be provided as input. Output from this transform process is 
in CSV format (with '|' as default delimiter).
\nUsage example:
    >> python transform.py -c .\configs\china\config.json
"""

HELP ="""[Required] Configuration file (with full or relative path).
E.g., python transform.py -c .\configs\china\config.json
"""


def _get_value_from_dict(dict, key, default_value):
    """
    Returns associated value of a given key from dict.
    If the key doesn't exist, returns default_value.
    """
    if dict.get(key) is None:
        return default_value
    elif (isinstance(dict.get(key), str)) and (not dict.get(key)):
        return default_value
    else:
        return dict.get(key)


def load_config(config_file):
    """
    Loads the config file as JSON.
    REF: https://web.archive.org/web/20181002170353/https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
    """
    with open(config_file, 'r') as f:
        return json.load(f)


def _assert_required_keys(config):
    """Checks if all required keys exist in the config loaded."""
    for k in REQUIRED_KEYS:
        if not k in config:
            raise transform_errors.RequiredKeyNotFoundInConfigFile(k)


def _assert_expected_data_types(config):
    """Checks if loaded config has values that are of expected data types."""
    for k, types in EXPECTED_CONFIG_DATA_TYPES.items():
        # we use 'any' because some of the keys be , for example,
        # either int or None, and EXPECTED_CONFIG_DATA_TYPES
        # can have something like {KEY_NAME : [int, None]}
        if not any([isinstance(config[k], t) for t in types]):
            raise transform_errors.InputDataTypeError(k, types)


def validate_configurations(config):
    """Calls other helper functions to check on the validity of config JSON"""
    _assert_required_keys(config)
    _assert_expected_data_types(config)


def get_input_files(config):
    """
    Returns input file(s) based on the file name/pattern
    in the input folder name provided in JSON config file.
    """
    fn = os.path.join(config[KEY_INPUT_FOLDER_PATH],
                      config[KEY_INPUT_FILE_NAME_OR_PATTERN])
    # REF: https://stackoverflow.com/a/41447012/1330974
    input_files = [str(f.absolute()) for f in pathlib.Path().glob(fn)]

    if not input_files:
        raise transform_errors.FileNotFound(fn)
    return input_files


def get_output_file_path_with_name_prefix(config):
    """
    Returns output file path with file name prefix, if the latter
    is provided in the config JSON. Before joining the path with
    file name, output folder is created if it doesn't exist already.
    """
    if not os.path.exists(config[KEY_OUTPUT_FOLDER_PATH]):
        os.makedirs(config[KEY_OUTPUT_FOLDER_PATH])
        print("\nINFO: new folder created for output files =>",
              config[KEY_OUTPUT_FOLDER_PATH])

    file_prefix =  config[KEY_OUTPUT_FILE_PREFIX] if KEY_OUTPUT_FILE_PREFIX in config else ''
    return os.path.join(config[KEY_OUTPUT_FOLDER_PATH], file_prefix)


def _append_sys_path(new_sys_path):
    if new_sys_path not in sys.path:
        sys.path.append(new_sys_path)
        print("\nNew sys path appended:", new_sys_path)
        print("Current sys path is:\n", sys.path, "\n")


# KEY_TRANSFORM_FUNCTIONS_FILE = 'transform_functions_files'
# # We will assume the transform_functions.py file is: './transform_functions/transform_functions.py'
# VALUE_TRANSFORM_FUNCTIONS_FILE_DEFAULT = os.path.join(os.getcwd(), 'transform_functions', 'transform_functions.py')
def load_transform_functions(config):
    """Extract corresponding value from config file and load the custom module that has transform functions.
    """
    transform_funcs_file = _get_value_from_dict(config,
                                                KEY_TRANSFORM_FUNCTIONS_FILE,
                                                VALUE_TRANSFORM_FUNCTIONS_FILES_DEFAULT)
    if os.path.isfile(transform_funcs_file):
        directory, file_name = os.path.split(transform_funcs_file)
        _append_sys_path(directory)

        file_name_without_extension = os.path.splitext(file_name)[0]
        # Note: we assume that all transform function modules are located in
        # './transform_funcs' directory, which is used as pcakage name below.
        # Module name is either country specific python file name (wihtout extension) or transform_funcs
        # E.g., importlib.import_module('switzerland_transform_functions', package='transform_functions')
        # OR importlib.import_module('transform_functions.switzerland_transform_functions')
        return importlib.import_module(file_name_without_extension,
                                       package=os.path.basename(directory))
    else:
        raise transform_errors.FileNotFound(transform_funcs_file)


def get_sheet_name(config):
    """
    Returns the sheet name from the config JSON.
    If the keys aren't defined in the JSON, returns default values
    ('Sheet1'), which means Pandas will load the first sheet in the Excel file.
    """
    return str(_get_value_from_dict(config,
                                    KEY_SHEET_NAME,
                                    VALUE_SHEET_NAME_DEFAULT))


def _extract_file_name(file_path_and_name):
    """Extracts file name from path+filename string."""
    return os.path.split(file_path_and_name)[-1]


def _get_file_extension(file_name):
    """Extracts file extension from filename string."""
    return os.path.splitext(file_name)[1]


def is_excel(file_name_with_path):
    """Checks if file is Excel file type."""
    file_extension = _get_file_extension(_extract_file_name(file_name_with_path))
    return ((EXCEL_FILE_EXTENSION_NEW == file_extension.lower()) or
            (EXCEL_FILE_EXTENSION_OLD == file_extension.lower()))


def is_csv(file_name_with_path):
    """Checks if file is CSV file type."""
    file_extension = _get_file_extension(_extract_file_name(file_name_with_path))
    return CSV_FILE_EXTENSION == file_extension.lower()


def read_data(file_name_with_path, config, rows_to_read,
              skip_leading_rows=0, skip_trailing_rows=0,
              header_row_index=0, custom_header_names=None,
              column_names_or_indexes_to_use=None,
              custom_data_types={}):
    """
    This function is used to get just one row, if any, that has column headers.

    :param file_name_with_path:
    :param config:
    :param rows_to_read:
    :param skip_leading_rows:
    :param skip_trailing_rows:
    :param header_row_index:
    :param custom_header_names:
    :param column_names_or_indexes_to_use:
    :param custom_data_types:
    :return:
    """
    if is_excel(file_name_with_path):
        return pd.read_excel(file_name_with_path,
                             skiprows=skip_leading_rows,
                             nrows=rows_to_read,
                             skipfooter=skip_trailing_rows,
                             header=header_row_index,
                             names=custom_header_names,
                             usecols=column_names_or_indexes_to_use,
                             dtype=custom_data_types,
                             sheet_name=get_sheet_name(config),
                             )
    elif is_csv(file_name_with_path):
        return pd.read_csv(file_name_with_path,
                           skiprows=skip_leading_rows,
                           # below causes error if we tries to read chunk=x and there's < x rows left in the last chunk
                           #nrows=rows_to_read,
                           chunksize=rows_to_read,
                           skipfooter=skip_trailing_rows,
                           header=header_row_index,
                           names=custom_header_names,
                           usecols=column_names_or_indexes_to_use,
                           dtype=custom_data_types,
                           delimiter=get_input_csv_delimiter(config),
                           encoding=get_input_csv_encoding(config),
                           # don't skip anything in input file and let programmer
                           # decide how to parse them later in transform_functions
                           #skip_blank_lines=False,
                           )
    else:
        raise transform_errors.InvalidFileType(file_name_with_path)


def _get_row_index_to_extract_column_headers(config):
    """
    Retrieves row number where we can fetch column headers
    in the input file. If the keys aren't defined in
    the JSON, returns 0 as default.
    """
    return _get_value_from_dict(config,
                                KEY_ROW_INDEX_OF_COLUMN_HEADERS,
                                VALUE_COLUMN_HEADER_ROW_NUM_DEFAULT)


def get_raw_column_headers(input_file, config):
    """
    Returns a list of column headers either from input file at specified
    row index or custom column names defined in JSON config file.

    Note: In pandas, we would read headers like below--
    df1=pd.read_csv('csv_n.csv',delimiter='|', header=0, nrows=0, skip_blank_lines=False)
    df2=pd.read_csv('csv_d.csv',delimiter='|', header=4, nrows=0, skip_blank_lines=False)
    df3=pd.read_excel('excel_n.xlsx', sheet_name=0, header=0, nrows=0)
    df4=pd.read_excel('excel_d.xlsx', sheet_name=0, header=4, nrows=0)
    """
    row_index_to_extract_column_headers = _get_row_index_to_extract_column_headers(config)

    if row_index_to_extract_column_headers >= 0:
        return read_data(input_file,
                         config,
                         0,  # to read just the column names, must leave this as 0
                         header_row_index=row_index_to_extract_column_headers,
                         ).columns.to_list()
    else:
        return None


def get_row_index_where_data_starts(config):
    """
    Returns the row index where the data lines begin in the input file.
    If key not provided in the JSON config file, returns 0 as default.
    """
    return _get_value_from_dict(config,
                                KEY_ROW_INDEX_WHERE_DATA_STARTS,
                                VALUE_ROW_INDEX_WHERE_DATA_STARTS_DEFAULT)


def get_number_of_rows_to_skip_from_bottom(config):
    """
    Returns number of rows we should ignore/skip at the bottom of
    the input file. If the key not provided in the JSON config file,
    returns 0 as default.
    """
    return _get_value_from_dict(config,
                                KEY_BOTTOM_ROWS_TO_SKIP,
                                VALUE_BOTTOM_ROWS_TO_SKIP_DEFAULT)


def get_number_of_rows_to_skip_from_bottom(config):
    """
    Returns number of rows we should ignore/skip at the bottom of
    the input file. If key is not provided in the JSON config file,
    returns 0 as default.
    """
    return _get_value_from_dict(config,
                                KEY_BOTTOM_ROWS_TO_SKIP,
                                VALUE_BOTTOM_ROWS_TO_SKIP_DEFAULT)


def get_rows_per_chunk_for_csv(config):
    """
    Returns number of rows we should process (read and write)
    per each iteration (for each input file). If the key is
    not provided in the JSON config file, returns
    VALUE_ROWS_PER_CHUNK_DEFAULT as default.
    """
    return _get_value_from_dict(config,
                                KEY_ROWS_PER_CHUNK_FOR_CSV,
                                VALUE_ROWS_PER_CHUNK_FOR_CSV_DEFAULT)


def get_input_csv_encoding(config):
    """
    Retrieves encoding for input CSV file.
    REF: https://docs.python.org/3/library/codecs.html#standard-encodings
    """
    return _get_value_from_dict(config,
                                KEY_INPUT_CSV_ENCODING,
                                VALUE_INPUT_CSV_ENCODING_DEFAULT)


def get_input_csv_delimiter(config):
    """Retrieves delimiter for input CSV file."""
    return _get_value_from_dict(config,
                                KEY_INPUT_CSV_DELIMITER,
                                VALUE_INPUT_CSV_DELIMITER_DEFAULT)


def get_output_csv_encoding(config):
    """
    Retrieves encoding for output CSV file.
    REF: https://docs.python.org/3/library/codecs.html#standard-encodings
    """
    return _get_value_from_dict(config,
                                KEY_OUTPUT_CSV_ENCODING,
                                VALUE_OUTPUT_CSV_ENCODING_DEFAULT)


def get_output_csv_delimiter(config):
    """Retrieves delimiter for output CSV file."""
    return _get_value_from_dict(config,
                                KEY_OUTPUT_CSV_DELIMITER,
                                VALUE_OUTPUT_CSV_DELIMITER_DEFAULT)
