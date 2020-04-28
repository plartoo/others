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

KEY_CUSTOM_FUNCTIONS_FILE = 'custom_transform_functions_file'
# We will assume the transform_functions.py file is: './transform_functions/transform_functions.py'
DEFAULT_COMMON_TRANSFORM_FUNCTIONS_FILE = os.path.join(os.getcwd(),
                                                       'transform_functions',
                                                       'transform_functions.py')

KEY_DATA_WRITER_CLASS_FILE = 'data_writer_class_file'
DEFAULT_DATA_WRITER_CLASS_FILE = os.path.join(os.getcwd(),
                                              'csv_data_writer.py')




### READER related constants. will be removed after refactoring
# Pandas unfortunately has 'keep_default_na' option which tries to interpret
# NaN, NULL, NA, N/A, etc. values in the raw data to NaN. We must turn it off
# by default. REF: https://stackoverflow.com/a/41417295
KEY_KEEP_DEFAULT_NA = 'interpret_na_null_etc_values_from_raw_data_as_nan'  # TODO: remove
DEFAULT_KEEP_DEFAULT_NA = False  # TODO: remove

KEY_ROW_INDEX_OF_COLUMN_HEADERS = 'row_index_to_extract_column_headers'  # TODO: remove
DEFAULT_COLUMN_HEADER_ROW_NUM = -1  # TODO: remove

KEY_INPUT_FOLDER_PATH = 'input_folder_path'
KEY_INPUT_FILE_NAME_OR_PATTERN = 'input_file_name_or_pattern'
KEY_WRITE_OUTPUT = 'write_output'
DEFAULT_WRITE_OUTPUT = True

KEY_SHEET_NAME_OF_INPUT_EXCEL_FILE = 'sheet_name_of_input_excel_file'  # TODO: remove
DEFAULT_SHEET_NAME_OF_INPUT_EXCEL_FILE = 0  # TODO: remove

KEY_ROWS_PER_READ_ITERATION = 'rows_per_read'
DEFAULT_ROWS_PER_READ_ITERATION = 500000
KEY_INPUT_FILE_ENCODING = 'input_file_encoding'
DEFAULT_INPUT_FILE_ENCODING = None  # None defaults to 'utf-8' in pandas
# Note: we tested and found that pandas' csv sniffer isn't very good
# (even when using 'Python' as parser engine) in detecting delimiters, so
# setting this as None is not good enough. Thus we decided to set the default
# for 'DEFAULT_INPUT_CSV_DELIMITER' as comma.
KEY_INPUT_CSV_DELIMITER = 'input_csv_file_delimiter'
DEFAULT_INPUT_CSV_DELIMITER = ','

KEY_ROW_INDEX_WHERE_DATA_STARTS = 'row_index_where_data_starts'
DEFAULT_ROW_INDEX_WHERE_DATA_STARTS = 1
KEY_BOTTOM_ROWS_TO_SKIP = 'num_of_rows_to_skip_from_the_bottom'
DEFAULT_BOTTOM_ROWS_TO_SKIP = 0



### WRITER related constants. will be removed after refactoring
KEY_DATABASE_SCHEMA = 'database_schema'  # TODO: map to mssql_data_writer
KEY_OUTPUT_TABLE_NAME = 'output_sql_table_name'  # TODO: map to mssql_data_writer
DEFAULT_OUTPUT_TABLE_NAME = 'default_transformed_sql_table_name'  # TODO: map to mssql_data_writer

KEY_OUTPUT_FILE_PREFIX = 'output_file_name_prefix'  # TODO: map to csv_data_writer and excel_data_writer
KEY_OUTPUT_FOLDER_PATH = 'output_folder_path'  # TODO: map to csv_data_writer and excel_data_writer
DEFAULT_OUTPUT_FOLDER_PATH = os.path.join(os.getcwd(),  # TODO: map to csv_data_writer and excel_data_writer
                                          'output')
KEY_SHEET_NAME_OF_OUTPUT_EXCEL_FILE = 'sheet_name_of_output_excel_file'  # TODO: map to excel_data_writer
DEFAULT_SHEET_NAME_OF_OUTPUT_EXCEL_FILE = 'Sheet1'  # TODO: map to excel_data_writer
KEY_OUTPUT_FILE_ENCODING = 'output_file_encoding'  # TODO: map to csv_data_writer and excel_data_writer
DEFAULT_OUTPUT_FILE_ENCODING = None  # None defaults to 'utf-8' in pandas # TODO: map to csv_data_writer and excel_data_writer
KEY_OUTPUT_CSV_DELIMITER = 'output_csv_file_delimiter'  # TODO: map to csv_data_writer
DEFAULT_OUTPUT_CSV_DELIMITER = '|'  # # TODO: map to csv_data_writer
KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE = 'include_index_column_in_output'  # TODO: map to mssql_data_writer, csv_data_writer, excel_data_writer
DEFAULT_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE = False  # TODO: map to mssql_data_writer, csv_data_writer, excel_data_writer





KEY_FUNCTIONS_TO_APPLY = 'functions_to_apply'
DEFAULT_FUNCTIONS_TO_APPLY = []
KEY_FUNC_NAME = 'function_name'
KEY_FUNC_ARGS = 'function_args'
DEFAULT_FUNC_ARGS = []
KEY_FUNC_KWARGS = 'function_kwargs'
DEFAULT_FUNC_KWARGS = {}

# Keys in config file and their expected data types
# TODO: review the list of expected data types below and enter the new ones I've included since January 2020
EXPECTED_CONFIG_DATA_TYPES = {
    KEY_INPUT_FOLDER_PATH: [str],
    KEY_INPUT_FILE_NAME_OR_PATTERN: [str],
    KEY_OUTPUT_FOLDER_PATH: [str],
    KEY_OUTPUT_FILE_PREFIX: [str],
    KEY_SHEET_NAME_OF_INPUT_EXCEL_FILE: [str],

    KEY_INPUT_FILE_ENCODING: [str],
    KEY_INPUT_CSV_DELIMITER: [str],
    KEY_OUTPUT_FILE_ENCODING: [str],
    KEY_OUTPUT_CSV_DELIMITER: [str],
    KEY_ROW_INDEX_OF_COLUMN_HEADERS: [int],
    KEY_ROW_INDEX_WHERE_DATA_STARTS: [int],
    KEY_BOTTOM_ROWS_TO_SKIP: [int],
    KEY_FUNCTIONS_TO_APPLY: [list],
    KEY_ROWS_PER_READ_ITERATION: [int],
}

# Keys in config file that must exist (required keys)
REQUIRED_KEYS = [KEY_INPUT_FOLDER_PATH,
                 KEY_INPUT_FILE_NAME_OR_PATTERN,
                 KEY_FUNCTIONS_TO_APPLY]


# TODO: remove this because now I'm 100% sure we are going to
#  go with JSON config and the keys are now only going to be
#  of string type. So delete this and its uses throughout the
#  codebase
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


def _append_sys_path(new_sys_path):
    if new_sys_path not in sys.path:
        sys.path.append(new_sys_path)
        print("\nThis new sys path is appended:", new_sys_path)
        print("Current sys path is:\n", sys.path, "\n")


def insert_input_file_keys_values_to_config_json(file_path_and_name, config):
    """
    Inserts input file's path and name as values to corresponding keys
    in config JSON. This method is called if user provides input file
    path and name info via commandline instead of via config file.

    This is more like a hack because feeding input file information via
    commandline is an afterthought (originally, I was not very keen on it,
    but then I realized if we are to use one common config file to do,
    for example, QA-testing of common patterns, this commandline feeding
    of input file name can be much neater than creating similar config
    file one per country.
    """
    config[KEY_INPUT_FOLDER_PATH] = os.path.split(file_path_and_name)[0]
    config[KEY_INPUT_FILE_NAME_OR_PATTERN] = os.path.split(file_path_and_name)[1]
    return config


def get_input_files(config):
    """
    Returns the input file(s) based on the file name/pattern
    in the input folder name provided in the JSON config file.
    """
    fn = os.path.join(config[KEY_INPUT_FOLDER_PATH],
                      config[KEY_INPUT_FILE_NAME_OR_PATTERN])
    # REF: https://stackoverflow.com/a/41447012/1330974
    input_files = [str(f.absolute()) for f in pathlib.Path().glob(fn)]

    if not input_files:
        raise transform_errors.FileNotFound(fn)
    return input_files


def get_input_file_sheet_name(config):
    """
    Returns the input file's sheet name from the config JSON.
    If the keys aren't defined in the JSON, returns default sheet
    (which is 0), which means Pandas will load the first sheet in
    Excel file.
    """
    return _get_value_from_dict(config,
                                KEY_SHEET_NAME_OF_INPUT_EXCEL_FILE,
                                DEFAULT_SHEET_NAME_OF_INPUT_EXCEL_FILE)


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
                                DEFAULT_KEEP_DEFAULT_NA)


# def get_output_file_sheet_name(config):
#     """
#     Returns the output file's sheet name from the config JSON.
#     If the keys aren't defined in the JSON, returns default sheet
#     (which is 'Sheet1'), which means Pandas will write to 'Sheet1'
#     in output Excel file.
#     """
#     return _get_value_from_dict(config,
#                                 KEY_SHEET_NAME_OF_OUTPUT_EXCEL_FILE,
#                                 DEFAULT_SHEET_NAME_OF_OUTPUT_EXCEL_FILE)


def _get_relative_module_name(module_file):
    """
    Suppose we want to load Python module file in this relative path:
    './transform_functions/swiss_transform_funcs.py', we can use
    'importlib.import_module(...)' method in one of the two ways below.
    1) import_module('.swiss_transform_funcs', package='transform_functions')
    or
    2) import_module('transform_functions.swiss_transform_funcs')

    Assuming that we will be using method signature #1 above,
    this method extracts and return relative module name (that is,
    '.swiss_transform_funcs') from path and name of a module file.
    """
    # directory, file_name = os.path.split(module_file)
    # file_name_without_extension = os.path.splitext(file_name)[0]
    # relative_module_name = ''.join(['.', file_name_without_extension])
    # package_name = os.path.basename(directory)
    file_name = os.path.split(module_file)[1]
    file_name_without_extension = os.path.splitext(file_name)[0]
    relative_module_name = ''.join(['.', file_name_without_extension])

    return relative_module_name


def _get_package_name(module_file):
    """
    Suppose we want to load Python module file in this relative path:
    './transform_functions/funcs/swiss_transform_funcs.py', we can use
    'importlib.import_module(...)' method in one of the two ways below.
    1) import_module('.swiss_transform_funcs', package='transform_functions')
    or
    2) import_module('transform_functions.swiss_transform_funcs')

    Assuming that we will be using method signature #1 above,
    this method extracts and return package name (that is,
    'transform_functions.funcs') from the path and name of a module file.
    """
    directory_path = os.path.split(os.path.relpath(module_file))[0]  # e.g., './transform_funcs/funcs'
    if directory_path.startswith('./') or directory_path.startswith('.\\'):
        directory_path = directory_path.replace('./', '').replace('.\\', '')

    return directory_path.replace('/', '.').replace('\\', '.')


def _instantiate_transform_module(transform_funcs_file, transform_funcs_module):
    if transform_funcs_file == DEFAULT_COMMON_TRANSFORM_FUNCTIONS_FILE:
        # Here, the config file does not define the file that has
        # custom transform functions, so we are going to load (instantiate)
        # the CommonTransformFunctions instance.
        return transform_funcs_module.CommonTransformFunctions()
    else:
        return transform_funcs_module.CustomFunctions()


def instantiate_custom_functions_module(config):
    """
    This function is used to load the module that includes
    all custom functions be it for data transformation or for
    data QA-ing.

    It first extracts the module's path+file name from the config
    file and imports the module that has either the custom functions
    or the common transform functions (default). After importing
    the module, this function instantiates and return that module
    as an object.
    """
    custom_funcs_file = _get_value_from_dict(config,
                                             KEY_CUSTOM_FUNCTIONS_FILE,
                                             DEFAULT_COMMON_TRANSFORM_FUNCTIONS_FILE)

    if os.path.isfile(custom_funcs_file):
        # Note: we assume that all transform function modules are located in
        # './transform_funcs' directory, which is used as package name below.
        # Relative module name, the first argument of import_module() below,
        # is either custom python file name (without extension) or
        # the file with common transform functions (that is,
        # 'transform_functions' python file) prefixed with '.' (dot).
        #
        # E.g., importlib.import_module('.switzerland_transform_functions', package='transform_functions')
        # OR importlib.import_module('transform_functions.switzerland_transform_functions')
        # REF1: https://stackoverflow.com/a/10675081/1330974
        # REF2: https://stackoverflow.com/a/8899345/1330974
        return _instantiate_transform_module(custom_funcs_file,
                                             importlib.import_module(
                                                 _get_relative_module_name(custom_funcs_file),
                                                 package=_get_package_name(custom_funcs_file)))
    else:
        raise transform_errors.FileNotFound(custom_funcs_file)


def get_write_data_decision(config):
    """
    Get boolean value that tells the program whether to
    write the output (transformed dataframe) to somewhere.
    """
    return _get_value_from_dict(config,
                                KEY_WRITE_OUTPUT,
                                DEFAULT_WRITE_OUTPUT)


def instantiate_data_writer_module(config):
    """
    This method will load the custom DataWriter module
    if path to the custom DataWriter class (such as DataWriter for
    SQL Server) is provided in the config file.
    If that key in config file is not given, this method will load
    default DataWriter module which will output CSV file for
    transformed data.
    Note: This method assumes that the DataWriter module file
    is located in the same root folder as 'transform.py' file.
    """
    data_writer_class_file = _get_value_from_dict(config,
                                                  KEY_DATA_WRITER_CLASS_FILE,
                                                  DEFAULT_DATA_WRITER_CLASS_FILE)
    if os.path.isfile(data_writer_class_file):
        # Note: we assume that all data writer modules are located in
        # the same root folder (i.e. 'data_transformer' folder).
        # Thus, we will call import_module() like below
        # importlib.import_module('.csv_data_writer')
        data_writer_module = importlib.import_module \
            (os.path.splitext(os.path.split(data_writer_class_file)[1])[0])

        return data_writer_module.DataWriter(config)
    else:
        raise transform_errors.FileNotFound(data_writer_class_file)


# def get_output_folder(config):
#     """
#     Extracts and return the output folder path and name from the
#     config JSON. If the keys aren't defined in the JSON config
#     file, this method returns default output folder ('./output')
#     name.
#     """
#     return _get_value_from_dict(config,
#                                 KEY_OUTPUT_FOLDER_PATH,
#                                 DEFAULT_OUTPUT_FOLDER_PATH)
#
#
# def get_output_file_prefix(config):
#     """
#     Extracts and return the output file prefix, if any, from
#     the config file. If not given, returns empty string.
#     """
#     return _get_value_from_dict(config,
#                                 KEY_OUTPUT_FILE_PREFIX,
#                                 '')

# def get_output_sql_table_name(config):
#     """
#     Extracts and return the output SQL table name, if provided,
#     from the config file. If not given, defaults to
#     DEFAULT_OUTPUT_TABLE_NAME defined in this (transform_utils.py)
#     file.
#     """
#     return _get_value_from_dict(config,
#                                 KEY_OUTPUT_TABLE_NAME,
#                                 DEFAULT_OUTPUT_TABLE_NAME)


# def get_database_schema(config):
#     """
#     Extracts and return the DB schema for output SQL table from
#     the config file. If not given, defaults to empty string.
#     """
#     return _get_value_from_dict(config,
#                                 KEY_DATABASE_SCHEMA,
#                                 '')


# def get_include_index_column_in_output(config):
#     """
#     Extracts and return boolean value to decide if output (be it,
#     CSV file or SQL table) should include index column from
#     the dataframe.
#     """
#     return _get_value_from_dict(config,
#                                 KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE,
#                                 DEFAULT_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE)

#
# def get_output_file_encoding(config):
#     """
#     Retrieves encoding for output CSV file.
#     REF: https://docs.python.org/3/library/codecs.html#standard-encodings
#     """
#     return _get_value_from_dict(config,
#                                 KEY_OUTPUT_FILE_ENCODING,
#                                 DEFAULT_OUTPUT_FILE_ENCODING)

# def get_output_csv_file_delimiter(config):
#     """Retrieves delimiter for output CSV file."""
#     return _get_value_from_dict(config,
#                                 KEY_OUTPUT_CSV_DELIMITER,
#                                 DEFAULT_OUTPUT_CSV_DELIMITER)

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
                             sheet_name=get_input_file_sheet_name(config),
                             )
    elif is_csv(file_name_with_path):
        return pd.read_csv(file_name_with_path,
                           skiprows=skip_leading_rows,
                           # below causes error if we tries to read chunk=x and there's < x rows left in the last chunk
                           # nrows=rows_to_read,
                           chunksize=rows_to_read,
                           skipfooter=skip_trailing_rows,
                           header=header_row_index,
                           names=custom_header_names,
                           usecols=column_names_or_indexes_to_use,
                           dtype=custom_data_types,
                           delimiter=get_input_csv_delimiter(config),
                           encoding=get_input_file_encoding(config),
                           # don't skip anything in input file and let programmer
                           # decide how to parse them later in transform_functions
                           # skip_blank_lines=False,
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
                                DEFAULT_COLUMN_HEADER_ROW_NUM)


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
                                DEFAULT_ROW_INDEX_WHERE_DATA_STARTS)


def get_number_of_rows_to_skip_from_bottom(config):
    """
    Returns number of rows we should ignore/skip at the bottom of
    the input file. If the key not provided in the JSON config file,
    returns 0 as default.
    """
    return _get_value_from_dict(config,
                                KEY_BOTTOM_ROWS_TO_SKIP,
                                DEFAULT_BOTTOM_ROWS_TO_SKIP)


def get_number_of_rows_to_skip_from_bottom(config):
    """
    Returns number of rows we should ignore/skip at the bottom of
    the input file. If key is not provided in the JSON config file,
    returns 0 as default.
    """
    return _get_value_from_dict(config,
                                KEY_BOTTOM_ROWS_TO_SKIP,
                                DEFAULT_BOTTOM_ROWS_TO_SKIP)


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
                                      DEFAULT_FUNCTIONS_TO_APPLY)
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
                                DEFAULT_FUNC_ARGS)


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
                                DEFAULT_FUNC_KWARGS)


def get_rows_per_chunk_for_csv(config):
    """
    Returns number of rows we should process (read and write)
    per each iteration (for each input file). If the key is
    not provided in the JSON config file, returns
    VALUE_ROWS_PER_CHUNK_DEFAULT as default.
    """
    return _get_value_from_dict(config,
                                KEY_ROWS_PER_READ_ITERATION,
                                DEFAULT_ROWS_PER_READ_ITERATION)


def get_input_file_encoding(config):
    """
    Retrieves encoding for input data file.
    REF: https://docs.python.org/3/library/codecs.html#standard-encodings
    """
    return _get_value_from_dict(config,
                                KEY_INPUT_FILE_ENCODING,
                                DEFAULT_INPUT_FILE_ENCODING)


def get_input_csv_delimiter(config):
    """Retrieves delimiter for input CSV file."""
    return _get_value_from_dict(config,
                                KEY_INPUT_CSV_DELIMITER,
                                DEFAULT_INPUT_CSV_DELIMITER)
