import pdb

import json
import sys

USAGE = '''
Usage example:
>> python transform.py -c .\configs\china\config.json
'''

DESC = "This program transform raw data files according to the procedures and rules" \
       "set forth in the JSON configuration file, which is provided as input.\n " \
       "The output from this transform process is in CSV format " \
       "(with '|' as default delimiter)." + USAGE

HELP = "[Required] Configuration file (with full/relative path).\n" \
       "E.g., python transform.py -c .\configs\china\config.json"

CONFIG_FILE_ERROR = '''
ERROR: You must provide a valid path AND name of the JSON configuration file.
''' + USAGE

DUPLICATE_SHEET_INDEX_ERROR = '''
ERROR: You can provide EITHER 'sheet_index_to_use' OR 'sheet_name_to_use' 
in the JSON configuration file. Not both. If you don't provide either,
the program will default to the first sheet in the file.
'''

DEFAULT_LABEL_SHEET_NAME = 'sheet_name_to_use'
DEFAULT_LABEL_SHEET_INDEX = 'sheet_index_to_use'
DEFAULT_VALUE_SHEET_INDEX = 0
DEFAULT_VALUE_SHEET_NAME = 'Sheet1'
DEFAULT_LABEL_LEADING_ROWS_TO_SKIP = 'leading_rows_to_skip'
DEFAULT_VALUE_LEADING_ROWS_TO_SKIP = 0
DEFAULT_LABEL_TRAILING_ROWS_TO_SKIP = 'trailing_rows_to_skip'
DEFAULT_VALUE_TRAILING_ROWS_TO_SKIP = 0

# TODO: write generate_config_json function below

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
    if (DEFAULT_LABEL_SHEET_NAME in config) and (DEFAULT_LABEL_SHEET_INDEX in config):
        sys.exit(DUPLICATE_SHEET_INDEX_ERROR)

    if DEFAULT_LABEL_SHEET_NAME in config:
        sheet = transform_utils.get_value_from_dict(
                                    config,
                                    transform_utils.DEFAULT_LABEL_SHEET_NAME,
                                    # we will just default to '0' value despite it being sheet name
                                    transform_utils.DEFAULT_VALUE_SHEET_INDEX)
    else:
        sheet = transform_utils.get_value_from_dict(
                                    config,
                                    transform_utils.DEFAULT_LABEL_SHEET_INDEX,
                                    transform_utils.DEFAULT_VALUE_SHEET_INDEX)
    return sheet


# def get_leading_rows_to_skip(config):
#     leading_rows_to_skip = get_value_from_dict(config, 'leading_rows_to_skip')
#     return DEFAULT_LEADING_ROWS_TO_SKIP if not leading_rows_to_skip else leading_rows_to_skip
#
#
# def get_trailing_rows_to_skip(config):
#     trailing_rows_to_skip = get_value_from_dict(config, 'trailing_rows_to_skip')
#     return DEFAULT_LEADING_ROWS_TO_SKIP if not trailing_rows_to_skip else trailing_rows_to_skip


def transform_utils():
    pass


def print_config():
    pass
