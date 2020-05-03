"""
Author: Phyo Thiha
Last Modified Date: April 22, 2020
"""
from datetime import datetime
import logging
import os


class PandasExcelDataReader:
    """
    This class uses Pandas read_excel to read Pandas dataframe
    from an Excel file. It supports several most commonly-used
    parameters of read_excel which are defined as class
    CONSTANTS below.
    """
    # Parameters supported from Pandas' read_excel method
    KEY_SHEET_NAME = 'sheet_name' # 'sheet_name_of_input_excel_file'
    DEFAULT_SHEET_TO_READ = 0

    KEY_KEEP_DEFAULT_NA = 'keep_default_na' # 'interpret_na_null_etc_values_from_raw_data_as_nan'
    DEFAULT_KEEP_DEFAULT_NA = False

    KEY_HEADER = 'header' # 'row_index_to_extract_column_headers'
    DEFAULT_HEADER = 0 # By default, assume first row as header row

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
