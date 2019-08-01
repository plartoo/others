import pdb

import json
import pathlib
import os
import sys

import transform_errors


ROWS_PER_CHUNK = 500000
ROWS_PER_FILE = 1500000

KEY_INPUT_FOLDER_PATH = 'input_folder_path'
KEY_INPUT_FILE_NAME_OR_PATTERN = 'input_file_name_or_pattern'
KEY_OUTPUT_FOLDER_PATH = 'output_folder_path'
KEY_OUTPUT_FILE_PREFIX = 'output_file_name_prefix'

KEY_COLUMN_HEADER_ROW_INDEX = "column_header_row_index"
KEY_CUSTOM_COLUMN_HEADER = "custom_column_headers"

KEY_SHEET_NAME = 'sheet_name_to_use'
KEY_SHEET_INDEX = 'sheet_index_to_use'
VALUE_SHEET_NAME_DEFAULT = 'Sheet1'
VALUE_SHEET_INDEX_DEFAULT = 0

KEY_COLUMN_NAMES_TO_USE = 'list_of_column_names_to_use'
KEY_COLUMN_INDEXES_TO_USE = 'list_of_column_indexes_to_use'
VALUE_COLUMNS_TO_USE_DEFAULT = None

KEY_LEADING_ROWS_TO_SKIP = 'leading_rows_to_skip'
KEY_STARTING_ROW_INDEX = 'starting_row_index_of_data'
KEY_TRAILING_ROWS_TO_SKIP = 'trailing_rows_to_skip'
VALUE_LEADING_ROWS_TO_SKIP_DEFAULT = 0
VALUE_STARTING_ROW_INDEX_DEFAULT = 0
VALUE_TRAILING_ROWS_TO_SKIP_DEFAULT = 0

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


def get_value_from_dict(dict, key, default_value):
    if dict.get(key) is None:
        return default_value
    elif (isinstance(dict.get(key), str)) and (not dict.get(key)):
        return default_value
    else:
        return dict.get(key)


def load_config(config_file):
    # REF: https://web.archive.org/web/20181002170353/https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
    with open(config_file, 'r') as f:
        return json.load(f)


def get_input_files(config):
    fn = os.path.join(config[KEY_INPUT_FOLDER_PATH],
                      config[KEY_INPUT_FILE_NAME_OR_PATTERN])
    # REF: https://stackoverflow.com/a/41447012/1330974
    input_files = [str(f.absolute()) for f in pathlib.Path().glob(fn)]

    if not input_files:
        raise transform_errors.FileNotFound(fn)
    return input_files


def get_output_file_prefix(config):
    if not os.path.exists(config[KEY_OUTPUT_FOLDER_PATH]):
        os.makedirs(config[KEY_OUTPUT_FOLDER_PATH])
        print("\nNote: new folder created for output files =>",
              config[KEY_OUTPUT_FOLDER_PATH])

    return os.path.join(config[KEY_OUTPUT_FOLDER_PATH],
                        config[KEY_OUTPUT_FILE_PREFIX])


def get_column_names_from_input_file(input_files, config):
    # KEY_COLUMN_HEADER_ROW_INDEX = "column_header_row_index"
    # KEY_CUSTOM_COLUMN_HEADER = "custom_column_headers"
    if (KEY_COLUMN_HEADER_ROW_INDEX in config) and (KEY_CUSTOM_COLUMN_HEADER in config):
        pass


# TODO: implementing now
def get_columns_to_use(config):
    KEY_COLUMN_NAMES_TO_USE = 'list_of_column_names_to_use'
    KEY_COLUMN_INDEXES_TO_USE = 'list_of_column_indexes_to_use'
    if (KEY_COLUMN_NAMES_TO_USE in config) and (KEY_COLUMN_INDEXES_TO_USE in config):
        raise transform_errors.RedundantJSONKeyError(KEY_COLUMN_NAMES_TO_USE,
                                                     KEY_COLUMN_INDEXES_TO_USE)

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

    # assert that the returned value is either None OR list
    if not list_of_columns_to_use:
        if not isinstance(list_of_columns_to_use, list):
            sys.exit(COLUMNS_TO_USE_TYPE_ERROR)

    return list_of_columns_to_use


# TODO: decide if to remove this function
def get_leading_rows_to_skip(config):
    return get_value_from_dict(
                config,
                KEY_LEADING_ROWS_TO_SKIP,
                VALUE_LEADING_ROWS_TO_SKIP_DEFAULT)


def get_starting_row_index(config):
    return get_value_from_dict(
                config,
                KEY_STARTING_ROW_INDEX,
                VALUE_STARTING_ROW_INDEX_DEFAULT)


def get_trailing_rows_to_skip(config):
    return get_value_from_dict(
                config,
                KEY_TRAILING_ROWS_TO_SKIP,
                VALUE_TRAILING_ROWS_TO_SKIP_DEFAULT)


def get_sheet_index_or_name(config):
    if (KEY_SHEET_NAME in config) and (KEY_SHEET_INDEX in config):
        raise transform_errors.RedundantJSONKeyError(KEY_SHEET_NAME,
                                                     KEY_SHEET_INDEX)

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
