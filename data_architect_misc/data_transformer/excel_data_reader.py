"""
Author: Phyo Thiha
Last Modified Date: April 22, 2020
"""
from datetime import datetime
import logging
import os

import transform_utils


class ExcelDataReader:
    """
    TODO 0: refactor CSV_data_writer and sql_server_data_writer as I did to excel_data_writer.py
    TODO 1: Write description here
    TODO 2: create a mapping of key names between transform and Excel Reader class in transform_utils.py

    """
    # Default params
    KEY_SHEET_NAME = 'sheet_name' # 'sheet_name_of_input_excel_file'
    DEFAULT_SHEET_TO_READ = 0

    # Optional params
    KEY_HEADER = 'header' # 'row_index_to_extract_column_headers'
    DEFAULT_HEADER = 0 # By default, assume first row as header row
    KEY_KEEP_DEFAULT_NA = 'keep_default_na' # 'interpret_na_null_etc_values_from_raw_data_as_nan'
    DEFAULT_KEEP_DEFAULT_NA = False
    KEY_ROWS_PER_READ_ITERATION = 'rows_per_read'
    DEFAULT_ROWS_PER_READ_ITERATION = 500000

    def __init__(self, input_file_path_and_name, configs):
        self.logger = logging.getLogger(__name__)
        import pdb
        pdb.set_trace()
        print("Hey it's Excel reader class")
        self.get_next_dataframe(input_file_path_and_name, configs)
        pass

    def get_next_dataframe(self, config):
        import pdb
        pdb.set_trace()
        print("Hey it's get_next_dataframe")


#col_headers_from_input_file = transform_utils.get_raw_column_headers(input_file, config)
