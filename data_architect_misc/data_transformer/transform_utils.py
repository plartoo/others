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

TRANSFORM_FUNCTIONS_FOLDER = 'transform_functions'
DEFAULT_COMMON_TRANSFORM_FUNCTIONS_FILE = 'transform_functions.py'
KEY_CUSTOM_TRANSFORM_FUNCTIONS_FILE = 'custom_transform_functions_file'
# We will assume the transform_functions.py file is: './transform_functions/transform_functions.py'
VALUE_COMMON_TRANSFORM_FUNCTIONS_FILE_DEFAULT = os.path.join(os.getcwd(),
                                                             TRANSFORM_FUNCTIONS_FOLDER,
                                                             DEFAULT_COMMON_TRANSFORM_FUNCTIONS_FILE)

KEY_SHEET_NAME = 'sheet_name_of_excel_file'
VALUE_SHEET_NAME_DEFAULT = 0
# Pandas unfortunately has 'keep_default_na' option which tries to interpret
# NaN, NULL, NA, N/A, etc. values in the raw data to NaN. We must turn it off
# by default. REF: https://stackoverflow.com/a/41417295
KEY_KEEP_DEFAULT_NA = 'interpret_na_null_etc_values_from_raw_data_as_nan'
VALUE_KEEP_DEFAULT_NA_DEFAULT = False

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

KEY_FUNCTIONS_TO_APPLY = 'functions_to_apply'
VALUE_FUNCTIONS_TO_APPLY = []
KEY_FUNC_NAME = 'function_name'
KEY_FUNC_ARGS = 'function_args'
VALUE_FUNC_ARGS_DEFAULT = []
KEY_FUNC_KWARGS = 'function_kwargs'
VALUE_FUNC_KWARGS_DEFAULT = {}

KEY_TRANSFORM_FUNC_NAME = 'transform_function_name'
KEY_TRANSFORM_FUNC_ARGS = 'transform_function_args'
VALUE_TRANSFORM_FUNC_ARGS_DEFAULT = []
KEY_TRANSFORM_FUNC_KWARGS = 'transform_function_kwargs'
VALUE_TRANSFORM_FUNC_KWARGS_DEFAULT = {}
KEY_ASSERT_FUNC_NAME = 'assert_function_name'
KEY_ASSERT_FUNC_ARGS = 'assert_function_args'
VALUE_ASSERT_FUNC_ARGS_DEFAULT = []
KEY_ASSERT_FUNC_KWARGS = 'assert_function_kwargs'
VALUE_ASSERT_FUNC_KWARGS_DEFAULT = {}

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
    KEY_FUNCTIONS_TO_APPLY: [list],
    KEY_ROWS_PER_CHUNK_FOR_CSV: [int],
}

# Keys in config file that must exist (required keys)
REQUIRED_KEYS = [KEY_INPUT_FOLDER_PATH,
                 KEY_INPUT_FILE_NAME_OR_PATTERN,
                 KEY_OUTPUT_FOLDER_PATH,
                 KEY_FUNCTIONS_TO_APPLY]

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


def _get_value_from_dict(dictionary, key, default_value):
    """
    Returns associated value of a given key from dict.
    If the key doesn't exist, returns default_value.
    """
    if dictionary.get(key) is None:
        return default_value
    elif (isinstance(dictionary.get(key), str)) and (not dictionary.get(key)):
        return default_value
    else:
        return dictionary.get(key)


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
        # We use 'any' because we want to allow some of the keys
        # to be, for example, either int or None, and
        # EXPECTED_CONFIG_DATA_TYPES can be configured with
        # something like {KEY_NAME : [int, None]}
        # print(k, "=>", config[k], "=>", types)
        if (k in config) and (not any([isinstance(config[k], t) for t in types])):
            raise transform_errors.ConfigFileInputDataTypeError(k, types)


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
        print("\nThis new sys path is appended:", new_sys_path)
        print("Current sys path is:\n", sys.path, "\n")


def _instantiate_transform_module(transform_funcs_file, transform_funcs_module):
    if transform_funcs_file == VALUE_COMMON_TRANSFORM_FUNCTIONS_FILE_DEFAULT:
        # Here, the config file does not define the file that has
        # custom transform functions, so we are going to load (instantiate)
        # the CommonTransformFunctions instance.
        return transform_funcs_module.CommonTransformFunctions()
    else:
        return transform_funcs_module.CustomTransformFunctions()


def instantiate_transform_functions_module(config):
    """First, extract corresponding value from config file and
    import the module that has either the common or the custom
    (e.g., transform) functions. After importing the module,
    call private function to instantiate that module.
    """
    transform_funcs_file = _get_value_from_dict(config,
                                                KEY_CUSTOM_TRANSFORM_FUNCTIONS_FILE,
                                                VALUE_COMMON_TRANSFORM_FUNCTIONS_FILE_DEFAULT)
    if os.path.isfile(transform_funcs_file):
        directory, file_name = os.path.split(transform_funcs_file)
        _append_sys_path(directory)

        file_name_without_extension = os.path.splitext(file_name)[0]
        relative_module_name = ''.join(['.', file_name_without_extension])
        # Note: we assume that all transform function modules are located in
        # './transform_funcs' directory, which is used as package name below.
        # Relative module name, the first argument, is either custom python file name
        # (without extension) or the file with common transform functions
        # (that is, 'transform_functions' python file) prefixed with '.' (dot).
        # E.g., importlib.import_module('switzerland_transform_functions', package='transform_functions')
        # OR importlib.import_module('transform_functions.switzerland_transform_functions')
        # REF1: https://stackoverflow.com/a/10675081/1330974
        # REF2: https://stackoverflow.com/a/8899345/1330974
        return _instantiate_transform_module(transform_funcs_file,
                                             importlib.import_module(
                                                 relative_module_name,
                                                 package=os.path.basename(directory)))
    else:
        raise transform_errors.FileNotFound(transform_funcs_file)


def get_sheet(config):
    """
    Returns the sheet name from the config JSON.
    If the keys aren't defined in the JSON, returns default sheet
    (which is 0), which means Pandas will load the first sheet in
    Excel file.
    """
    return _get_value_from_dict(config,
                                KEY_SHEET_NAME,
                                VALUE_SHEET_NAME_DEFAULT)


def get_keep_default_na(config):
    """
    Pandas somehow decided that it's okay to try to interpret
    values like 'NA','N/A','NULL','NaN', etc. to NaN value
    by default (that is, 'keep_default_na' option in pandas'
    read_excel/read_csv methods is True by default).

    So when we read raw data files using pandas, we must turn
    it off by default unless user explicitly set this flag to
    True.
    REF: https://stackoverflow.com/q/41417214
    """
    return _get_value_from_dict(config,
                                KEY_KEEP_DEFAULT_NA,
                                VALUE_KEEP_DEFAULT_NA_DEFAULT)


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
    TODO: We need to revise this for reading CSV header. Also review both approaches to see if we can simplify this.
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
                             sheet_name=get_sheet(config),
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


def _is_key_in_dict(dictionary, list_of_keys):
    """
    Checks to see if any of the keys in 'list_of_keys' is present
    in the dictionary. Returns True if at least one keys in the list
    exists in the dictionary. Otherwise, returns False.

    Args:
        dictionary: Dictionary to inspect the keys.
        list_of_keys:   List of keys (e.g., ['key1','key2']) that should be
                        present in the dictionary.

    Returns:
        True or False depending on if any of the key(s) exist in the dictionary.
    """
    return any(k in dictionary for k in list_of_keys)


def get_functions_to_apply(config):
    """
    Returns the list of dicts where each dict follows structure like
    below to embed each transform/assert function and its parameters:
    [
        {
            "transform_function_name": "drop_columns",
            "transform_function_args, [[1,2,3]],
            "transform_function_kwargs, {"key1":"val1", "key2":"val2"},
        },
        {
            "assert_function_name": "drop_columns",
            "assert_function_args, [[1,2,3]],
            "assert_function_kwargs, {"key1":"val1", "key2":"val2"},
        },
    ]
    """
    funcs_list = _get_value_from_dict(config,
                                      KEY_FUNCTIONS_TO_APPLY,
                                      VALUE_FUNCTIONS_TO_APPLY)
    if not funcs_list:
        # Function list must NOT be empty
        raise transform_errors.ListEmptyError(KEY_FUNCTIONS_TO_APPLY)

    for func_and_var in funcs_list:
        if type(func_and_var) is not dict:
            # Function and their corresponding parameters should be wrapped
            # in a dictionary as described in the documentation above.
            # E.g., [{"transform_function_name": "func_1", "transform_function_args": [[12]]}, ...]
            raise transform_errors.ConfigFileInputDataTypeError(KEY_FUNCTIONS_TO_APPLY, [dict])

    return funcs_list


def get_function_name(dict_of_func_and_params):
    """
    Extract and return function name (string type) from the dictionary
    that holds the function name and parameters (args/kwargs), if any.

    Args:
        dict_of_func_and_params: Dictionary that has function name and
        parameters like this:
          {
            "__function_comment__": "Drop empty columns in Budget roll up Excel file.",
            "function_name": "drop_unnamed_columns",
            "function_args": [["Unnamed 1", "Unnamed 2"]]
          }

    Returns:
         Function name (string) that we will convert to class attribute and invoke
         for data transformation.

    Raises:
        RequiredKeyNotFound: Return this error if there is no expected function key
        in the dictionary.
    """
    if not _is_key_in_dict(dict_of_func_and_params, [KEY_FUNC_NAME]):
        # This means the user did not not provide function name
        # for us to apply in the transform process
        raise transform_errors.RequiredKeyNotFound(dict_of_func_and_params,
                                                   [KEY_FUNC_NAME])

    return _get_value_from_dict(dict_of_func_and_params,
                                KEY_FUNC_NAME,
                                None)


# def get_transform_function_name(dict_of_func_and_params):
#     """
#     Extract and return function name (string type) from the dictionary
#     that holds transform function name and parameters (args/kwargs), if any.
#
#     Args:
#         dict_of_func_and_params: Dictionary that has function name and
#         parameters like this:
#           {
#             "__function_comment__": "Drop empty columns in Budget roll up Excel file.",
#             "transform_function_name": "drop_unnamed_columns",
#             "transform_function_args": [["Unnamed 1", "Unnamed 2"]]
#           }
#
#     Returns:
#          Function name (string) that we will convert to attribute and invoke
#          for data transformation.
#
#     Raises:
#         RequiredKeyNotFound: Return this error if there is no expected function key
#         in the dictionary.
#     """
#     if not _is_key_in_dict(dict_of_func_and_params, [KEY_TRANSFORM_FUNC_NAME]):
#         # This means the user did not not provide function name
#         # for us to apply in the transform process
#         raise transform_errors.RequiredKeyNotFound(dict_of_func_and_params,
#                                                    [KEY_TRANSFORM_FUNC_NAME])
#
#     return _get_value_from_dict(dict_of_func_and_params,
#                                 KEY_TRANSFORM_FUNC_NAME,
#                                 None)
#
#
# def get_assert_function_name(dict_of_func_and_params):
#     """
#     Extract and return function name (string type) from the dictionary
#     that holds assert function name and parameters (args/kwargs), if any.
#
#     Args:
#         dict_of_func_and_params: Dictionary that has function name and
#         parameters like this:
#           {
#             "__function_comment__": "Make sure the dataframe has 13 columns at this stage.",
#             "assert_function_name": "assert_number_of_columns_equals",
#             "assert_function_args": [10]
#           }
#
#     Returns:
#          Function name (string) that we will convert to attribute and invoke
#          for data QA (assertions).
#
#     Raises:
#         RequiredKeyNotFound: Return this error if there is no expected function key
#         in the dictionary.
#     """
#     if not _is_key_in_dict(dict_of_func_and_params, [KEY_ASSERT_FUNC_NAME]):
#         # This means the user did not not provide function name
#         # for us to apply in the transform process
#         raise transform_errors.RequiredKeyNotFound(dict_of_func_and_params,
#                                                    [KEY_ASSERT_FUNC_NAME])
#
#     return _get_value_from_dict(dict_of_func_and_params,
#                                 KEY_ASSERT_FUNC_NAME,
#                                 None)


def get_function_args(dict_of_func_and_params):
    """
    Extract and return list of arguments (*args) or an empty
    list from the dictionary that holds function name and
    parameters (args and kwargs), if any.

    Args:
        dict_of_func_and_params: Dictionary that has function name and
        parameters like this:
          {
            "__function_comment__": "Drop empty columns in Budget roll up Excel file.",
            "function_name": "drop_unnamed_columns",
            "function_args": [["Unnamed 1", "Unnamed 2"]]
          }

    Returns:
         List of parameters like [param1, param2] or an empty list if
         "function_args" key does not exists in the dictionary.
    """
    return _get_value_from_dict(dict_of_func_and_params,
                                KEY_FUNC_ARGS,
                                VALUE_FUNC_ARGS_DEFAULT)


def get_function_kwargs(dict_of_func_and_params):
    """
    Extract and return list of keyword arguments (*kwargs) or an empty list
    from the dictionary that holds function name and parameters
    (args and kwargs), if any.

    Args:
        dict_of_func_and_params: Dictionary that has function name and
        parameters like this:
          {
            "__function_comment__": "Drop empty columns in Budget roll up Excel file.",
            "function_name": "map_channel_columns",
            "function_kwargs": {"Amazon": "E-Commerce", "Ecommerce": "E-Commerce"}
          }

    Returns:
         Dictionary of keyword parameters like {"col1": "mapped_col_1", "col2": "mapped_col_2"}
         or an empty dictionary if "function_kwargs" key does not exist in the dictionary.
    """
    return _get_value_from_dict(dict_of_func_and_params,
                                KEY_FUNC_KWARGS,
                                VALUE_FUNC_KWARGS_DEFAULT)


# def get_transform_function_args(dict_of_func_and_params):
#     """
#     Extract and return list of arguments (*args) or an empty list from
#     the dictionary that holds transform function name and parameters
#     (args and kwargs), if any.
#
#     Args:
#         dict_of_func_and_params: Dictionary that has function name and
#         parameters like this:
#           {
#             "__function_comment__": "Drop empty columns in Budget roll up Excel file.",
#             "transform_function_name": "drop_unnamed_columns",
#             "transform_function_args": [["Unnamed 1", "Unnamed 2"]]
#           }
#
#     Returns:
#          List of parameters like [param1, param2] or an empty list.
#     """
#     return _get_value_from_dict(dict_of_func_and_params,
#                                 KEY_TRANSFORM_FUNC_ARGS,
#                                 VALUE_TRANSFORM_FUNC_ARGS_DEFAULT)
#
#
# def get_transform_function_kwargs(dict_of_func_and_params):
#     """
#     Extract and return list of keyword arguments (*kwargs) or an empty list
#     from the dictionary that holds transform function name and parameters
#     (args and kwargs), if any.
#
#     Args:
#         dict_of_func_and_params: Dictionary that has function name and
#         parameters like this:
#           {
#             "__function_comment__": "Drop empty columns in Budget roll up Excel file.",
#             "transform_function_name": "map_channel_columns",
#             "transform_function_kwargs": {"Amazon": "E-Commerce", "Ecommerce": "E-Commerce"}
#           }
#
#     Returns:
#          Dictionary of keyword parameters like {"col1": "mapped_col_1", "col2": "mapped_col_2"}
#          or an empty dictionary.
#     """
#     return _get_value_from_dict(dict_of_func_and_params,
#                                 KEY_TRANSFORM_FUNC_KWARGS,
#                                 VALUE_TRANSFORM_FUNC_KWARGS_DEFAULT)
#
#
# def get_assert_function_args(dict_of_func_and_params):
#     """
#     Extract and return list of arguments (*args) or an empty list from
#     the dictionary that holds assert function name and parameters
#     (args and kwargs), if any.
#
#     Args:
#         dict_of_func_and_params: Dictionary that has function name and
#         parameters like this:
#           {
#             "__function_comment__": "Make sure the dataframe has 13 columns at this stage.",
#             "assert_function_name": "assert_number_of_columns_equals",
#             "assert_function_args": [10]
#           }
#
#     Returns:
#          List of parameters like [param1, param2] or an empty list.
#     """
#     return _get_value_from_dict(dict_of_func_and_params,
#                                 KEY_ASSERT_FUNC_ARGS,
#                                 VALUE_ASSERT_FUNC_ARGS_DEFAULT)
#
#
# def get_assert_function_kwargs(dict_of_func_and_params):
#     """
#     Extract and return list of keyword arguments (*kwargs) or an empty list
#     from the dictionary that holds assert function name and parameters
#     (args and kwargs), if any.
#
#     Args:
#         dict_of_func_and_params: Dictionary that has function name and
#         parameters like this:
#           {
#             "__function_comment__": "Make sure if col1 is 'Amazon', col2's vlaue is 'E-Commerce'.",
#             "transform_function_name": "assert_mapped_channel_columns",
#             "transform_function_kwargs": {"Amazon": "E-Commerce"}
#           }
#
#     Returns:
#          Dictionary of keyword parameters like {"col1": "mapped_col_1", "col2": "mapped_col_2"}
#          or an empty dictionary.
#     """
#     return _get_value_from_dict(dict_of_func_and_params,
#                                 KEY_ASSERT_FUNC_KWARGS,
#                                 VALUE_ASSERT_FUNC_KWARGS_DEFAULT)


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
