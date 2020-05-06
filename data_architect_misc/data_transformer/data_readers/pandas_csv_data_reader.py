"""
Author: Phyo Thiha
Last Modified Date: April 22, 2020
"""
import logging

import pandas as pd
from rich import print

from data_readers.pandas_file_data_reader import PandasFileDataReader


class PandasCSVDataReader(PandasFileDataReader):
    """
    This class uses Pandas read_csv to read Pandas dataframe
    from a CSV file. It supports some most commonly-used
    parameters of read_csv which are defined as class
    CONSTANTS below.
    """
    KEY_INPUT_CSV_DELIMITER = 'input_delimiter'
    DEFAULT_INPUT_CSV_DELIMITER = ','

    # Best leave default as None for encoding
    # because it defaults to 'utf-8'
    # in Pandas's read_csv method
    KEY_OUTPUT_FILE_ENCODING = 'input_encoding'
    DEFAULT_OUTPUT_FILE_ENCODING = None

    def __init__(self, input_file_path_and_name, config):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.input_file = input_file_path_and_name
        self.sheet_name = self._get_sheet_name(config)
        self.header_row = self.read_header_row()
        # Number of times read_next_dataframe is called
        self.read_iter_count = 0

# TODO: finish csv0_config.json and its siblings (including CSV files)
# TODO: investigate what other options are available for encoding other than 'utf-8'
# TODO: does encoding=None default to utf-8?
