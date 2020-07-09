"""
This file compiles different constants that are used in
transform.py and transform_utils.py, and the ones that
are exposed to the user of transform.py script via JSON
config file. By compiling them in one place like this,
it help code reader as well as the user of transform.py
script to understand which keys they can define in the
config file.

Author: Phyo Thiha
Last Modified: May 9, 2020
"""
import os

from data_readers.pandas_file_data_reader import PandasFileDataReader
from data_readers.pandas_excel_data_reader import PandasExcelDataReader
from data_readers.pandas_csv_data_reader import PandasCSVDataReader
from data_writers.file_data_writer import FileDataWriter
from data_writers.excel_data_writer import ExcelDataWriter
from data_writers.csv_data_writer import CSVDataWriter
from data_writers.mssql_data_writer import MSSQLDataWriter

# transform.py and transform_utils.py will allow
# processing of more than one input files. Then we feed
# the combined folder+file name to data reader modules.
KEY_INPUT_FOLDER_PATH = 'input_folder_path'
KEY_INPUT_FILE_NAME_OR_PATTERN = 'input_file_name_or_pattern'

KEY_WRITE_OUTPUT = 'write_output'
DEFAULT_WRITE_OUTPUT = True
KEY_DATA_WRITER_MODULE_FILE = 'data_writer_module_file'
DEFAULT_DATA_WRITER_MODULE_FILE = os.path.join(os.getcwd(),
                                               'data_writers',
                                               'csv_data_writer.py')

KEY_CUSTOM_TRANSFORM_FUNCTIONS_FILE = 'custom_transform_functions_file'
DEFAULT_COMMON_TRANSFORM_FUNCTIONS_FILE = os.path.join(os.getcwd(),
                                                       'transform_functions',
                                                       'common_transform_functions.py')
KEY_FUNCTIONS_TO_APPLY = 'functions_to_apply'
KEY_FUNC_NAME = 'function_name'
KEY_FUNC_ARGS = 'function_args'
KEY_FUNC_KWARGS = 'function_kwargs'

# Keys in config file are required
REQUIRED_KEYS = [KEY_INPUT_FOLDER_PATH,
                 KEY_INPUT_FILE_NAME_OR_PATTERN,
                 KEY_FUNCTIONS_TO_APPLY]

# Keys in config file and their expected data types
# Note: In the future, we may want to allow some of
# the keys to be, for example, either of int or
# str type and that's why, the data types are
# described in a list below.
EXPECTED_CONFIG_VALUE_DATA_TYPES = {
    KEY_INPUT_FOLDER_PATH: [str],
    KEY_INPUT_FILE_NAME_OR_PATTERN: [str],
    KEY_WRITE_OUTPUT: [bool],
    KEY_DATA_WRITER_MODULE_FILE: [str],
    KEY_CUSTOM_TRANSFORM_FUNCTIONS_FILE: [str],
    KEY_FUNCTIONS_TO_APPLY: [list],

    # Data reader modules' constants
    PandasFileDataReader.KEY_ROWS_PER_READ: [int],
    PandasFileDataReader.KEY_KEEP_DEFAULT_NA: [bool],
    PandasFileDataReader.KEY_HEADER: [int],
    PandasFileDataReader.KEY_SKIP_ROWS: [int],
    PandasFileDataReader.KEY_SKIP_FOOTER: [int],
    PandasExcelDataReader.KEY_SHEET_NAME: [str, int, type(None)],
    PandasCSVDataReader.KEY_INPUT_CSV_DELIMITER: [str],
    PandasCSVDataReader.KEY_INPUT_FILE_ENCODING: [str],
    PandasCSVDataReader.KEY_SKIP_BLANK_LINES: [bool],

    # Data writer modules' constants
    FileDataWriter.KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE: [bool],
    FileDataWriter.KEY_OUTPUT_FOLDER_PATH: [str],
    FileDataWriter.KEY_OUTPUT_FILE_PREFIX: [str],
    FileDataWriter.KEY_OUTPUT_FILE_SUFFIX: [str],
    FileDataWriter.KEY_OUTPUT_FILE_ENCODING: [str],
    ExcelDataWriter.KEY_OUTPUT_SHEET_NAME: [str],
    CSVDataWriter.KEY_OUTPUT_DELIMITER: [str],
    MSSQLDataWriter.KEY_DATABASE_SCHEMA: [str],
    MSSQLDataWriter.KEY_OUTPUT_TABLE_NAME: [str],
    MSSQLDataWriter.KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE: [bool],
}

# The lists below are not used; I decided to group them together
# for code readers to have a clearer idea of how things
# are organized
READER_CONSTANTS = [
    PandasFileDataReader.KEY_ROWS_PER_READ,
    PandasFileDataReader.KEY_KEEP_DEFAULT_NA,
    PandasFileDataReader.KEY_HEADER,
    PandasFileDataReader.KEY_SKIP_ROWS,
    PandasFileDataReader.KEY_SKIP_FOOTER,

    PandasExcelDataReader.KEY_SHEET_NAME,

    PandasCSVDataReader.KEY_INPUT_CSV_DELIMITER,
    PandasCSVDataReader.KEY_INPUT_FILE_ENCODING,
    PandasCSVDataReader.KEY_SKIP_BLANK_LINES
]

WRITER_CONSTANTS = [
    FileDataWriter.KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE,
    FileDataWriter.KEY_OUTPUT_FOLDER_PATH,
    FileDataWriter.KEY_OUTPUT_FILE_PREFIX,
    FileDataWriter.KEY_OUTPUT_FILE_SUFFIX,
    FileDataWriter.KEY_OUTPUT_FILE_ENCODING,

    ExcelDataWriter.KEY_OUTPUT_SHEET_NAME,

    CSVDataWriter.KEY_OUTPUT_DELIMITER,

    MSSQLDataWriter.KEY_DATABASE_SCHEMA,
    MSSQLDataWriter.KEY_OUTPUT_TABLE_NAME,
    MSSQLDataWriter.KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE
]

# These constants below are used in transform.py
# to pass JSON configs between transform functions
KEY_CURRENT_INPUT_FILE = 'current_input_file'
KEY_HEADER = PandasFileDataReader.KEY_HEADER
KEY_DELIMITER = PandasCSVDataReader.KEY_INPUT_CSV_DELIMITER
