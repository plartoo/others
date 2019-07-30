import pdb

import json
import os
import sys

KEY_SHEET_NAME = 'sheet_name_to_use'
KEY_SHEET_INDEX = 'sheet_index_to_use'
VALUE_SHEET_NAME_DEFAULT = 'Sheet1'
VALUE_SHEET_INDEX_DEFAULT = 0

KEY_COLUMN_NAMES_TO_USE = 'list_of_column_names_to_use'
KEY_COLUMN_INDEXES_TO_USE = 'list_of_column_indexes_to_use'
VALUE_COLUMNS_TO_USE_DEFAULT = None

KEY_LEADING_ROWS_TO_SKIP = 'leading_rows_to_skip'
KEY_TRAILING_ROWS_TO_SKIP = 'trailing_rows_to_skip'
VALUE_ROWS_TO_SKIP_DEFAULT = 0

KEY_CSV_ENCODING = 'input_csv_file_encoding'
VALUE_CSV_ENCODING = None # None defaults to 'utf-8' in pandas

CSV_FILE_EXTENSION = '.csv'
EXCEL_FILE_EXTENSION_OLD = '.xls'
EXCEL_FILE_EXTENSION_NEW = '.xlsx'

USAGE = """\nUsage example:
        >> python transform.py -c .\configs\china\config.json"""

DESC = """This program transform raw data files according to the
       procedures and rules set forth in the JSON configuration file,
       which is provided as input. The output from this transform
       process is in CSV format (with '|' as default delimiter). """ + USAGE

HELP = """[Required] Configuration file (with full/relative path).
E.g., python transform.py -c .\configs\china\config.json"""

CONFIG_FILE_ERROR = """ERROR: You must provide a valid path 
AND name of the JSON configuration file. """ + USAGE

FILE_NOT_EXIST_ERROR = "ERROR: this file does not exist:"

FILE_TYPE_NOT_RECOGNIZED_ERROR = """ERROR: program does not know how to 
process this type of file extension for input file:"""

SHEET_KEYS_ERROR = """ERROR: You can provide EITHER """ \
                   + KEY_SHEET_NAME + """ OR """ \
                   + KEY_SHEET_INDEX \
                   + """in the JSON configuration file. Not both. 
                   If you don't provide either, the program will 
                   default to the first sheet in the file."""

COLUMNS_TO_USE_KEYS_ERROR = """ERROR: You can provide EITHER """ \
                   + KEY_COLUMN_NAMES_TO_USE + """ OR """ \
                   + KEY_COLUMN_INDEXES_TO_USE \
                   + """in the JSON configuration file. Not both. 
                   If you don't provide either, the program will 
                   parse ALL columns in the file."""

COLUMNS_TO_USE_TYPE_ERROR = """ERROR: For '""" + KEY_COLUMN_NAMES_TO_USE
+ """' and '""" + KEY_COLUMN_INDEXES_TO_USE + """' keys in JSON 
configuration file, you must provide either 'None' OR 
a list (of *all* strings or *all* integers) for their corresponding values"""

# TODO: write generate_config_json function below
# TODO: document methods
# TODO: unit test functions
# TODO: use pydoc to generate documentation

# def read_excel_file(file_path_and_name, sheet_name=0, header=0,
#                     skiprows=0, skipfooter=0):
#     t1 = time.time()
#     df = pd.read_excel(file_path_and_name, sheet_name=sheet_name,
#                        header=header, skiprows=skiprows, skipfooter=skipfooter)
#     print('Read Excel file:', file_path_and_name)
#     print("It took this many seconds to read the file:", time.time() - t1, "\n")
#     return df


def load_config(config_file):
    # REF: https://web.archive.org/web/20181002170353/https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
    with open(config_file, 'r') as f:
        return json.load(f)


def get_value_from_dict(dict, key, default_value):
    if dict.get(key) is None:
        return default_value
    elif (isinstance(dict.get(key), str)) and (not dict.get(key)):
        return default_value
    else:
        return dict.get(key)


def get_sheet_index_or_name(config):
    if (KEY_SHEET_NAME in config) and (KEY_SHEET_INDEX in config):
        sys.exit(SHEET_KEYS_ERROR)

    if KEY_SHEET_NAME in config:
        return str(
                    get_value_from_dict(
                        config,
                        KEY_SHEET_NAME,
                        VALUE_SHEET_NAME_DEFAULT)
        )
    else:
        return int(
                    get_value_from_dict(
                        config,
                        KEY_SHEET_INDEX,
                        VALUE_SHEET_INDEX_DEFAULT)
        )


def get_list_of_columns_to_use(config):
    if (KEY_COLUMN_NAMES_TO_USE in config) and (KEY_COLUMN_INDEXES_TO_USE in config):
        sys.exit(COLUMNS_TO_USE_KEYS_ERROR)

    if KEY_COLUMN_NAMES_TO_USE in config:
        list_of_columns_to_use = get_value_from_dict(
                                    config,
                                    KEY_COLUMN_NAMES_TO_USE,
                                    VALUE_COLUMNS_TO_USE_DEFAULT)
    else:
        list_of_columns_to_use = get_value_from_dict(
                                    config,
                                    KEY_COLUMN_INDEXES_TO_USE,
                                    VALUE_COLUMNS_TO_USE_DEFAULT)

    # make sure the returned value is either None OR a list
    if list_of_columns_to_use is not VALUE_COLUMNS_TO_USE_DEFAULT:
        if not isinstance(list_of_columns_to_use, list):
            sys.exit(COLUMNS_TO_USE_TYPE_ERROR)

    return list_of_columns_to_use


def get_leading_rows_to_skip(config):
    return get_value_from_dict(
                config,
                KEY_LEADING_ROWS_TO_SKIP,
                VALUE_ROWS_TO_SKIP_DEFAULT)


def get_trailing_rows_to_skip(config):
    return get_value_from_dict(
                config,
                KEY_TRAILING_ROWS_TO_SKIP,
                VALUE_ROWS_TO_SKIP_DEFAULT)


def extract_file_name(file_path_and_name):
    return os.path.split(file_path_and_name)[-1]


def get_file_extension(file_name):
    return os.path.splitext(file_name)[1]


def is_excel(file_name_with_path):
    file_extension = get_file_extension(extract_file_name(file_name_with_path))
    return ((EXCEL_FILE_EXTENSION_NEW == file_extension.lower()) or
            (EXCEL_FILE_EXTENSION_OLD == file_extension.lower()))


def is_csv(file_name_with_path):
    file_extension = get_file_extension(extract_file_name(file_name_with_path))
    return CSV_FILE_EXTENSION == file_extension.lower()


def get_csv_encoding(config):
    # REF: https://docs.python.org/3/library/codecs.html#standard-encodings
    return get_value_from_dict(
                config,
                KEY_CSV_ENCODING,
                VALUE_CSV_ENCODING)


def get_csv_delimiter(config):
    pass


def print_config():
    pass
