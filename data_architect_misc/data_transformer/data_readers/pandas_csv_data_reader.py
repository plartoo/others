"""
Author: Phyo Thiha
Last Modified Date: May 06, 2020
"""
import logging

import pandas as pd
from pandas.errors import EmptyDataError

from data_readers.pandas_file_data_reader import PandasFileDataReader


class PandasCSVDataReader(PandasFileDataReader):
    """
    This class uses Pandas read_csv to read Pandas dataframe
    from a CSV file. It supports some most commonly-used
    parameters of read_csv which are defined as class
    CONSTANTS below.
    """
    # Note: we tested and found that pandas' csv sniffer
    # isn't very good (even when using 'Python' as parser engine)
    # in detecting delimiters, so setting the default input csv
    # delimiter to None is not good enough. So, we settled on
    # the default as 'comma'.
    KEY_INPUT_CSV_DELIMITER = 'input_delimiter'
    DEFAULT_INPUT_CSV_DELIMITER = ','

    # Best leave default as None for encoding
    # because it defaults to 'utf-8'
    # in Pandas's read_csv method
    # For full list of encoding available in Pandas/Python
    # REF: https://docs.python.org/3/library/codecs.html#standard-encodings
    KEY_INPUT_FILE_ENCODING = 'input_encoding'
    DEFAULT_INPUT_FILE_ENCODING = None

    # Should CSV reader skip blank lines
    KEY_SKIP_BLANK_LINES = 'skip_blank_lines'
    DEFAULT_SKIP_BLANK_LINES = False

    def __init__(self, input_file_path_and_name, config):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.input_file = input_file_path_and_name
        self.delimiter = config.get(self.KEY_INPUT_CSV_DELIMITER,
                                    self.DEFAULT_INPUT_CSV_DELIMITER)
        # I'm aware that dict.get() returns None if key doesn't exist
        # but I'm expecting that we might some day use default
        # as something else. Then, we need DEFAULT_INPUT_FILE_ENCODING.
        self.encoding = config.get(self.KEY_INPUT_FILE_ENCODING,
                                   self.DEFAULT_INPUT_FILE_ENCODING)
        self.skip_blank_lines = config.get(self.KEY_SKIP_BLANK_LINES,
                                           self.DEFAULT_SKIP_BLANK_LINES)
        self.headers = self.read_header_row()
        # Number of times read_next_dataframe is called
        self.read_iter_count = 0

    def read_header_row(self):
        """
        Reads the row which has column headers
        and returns them as a list.

        If user instructed to not read header row
        (i.e. set 'header' key's value in config to
        None or did not provide 'header' key at all),
        this will return [0, 1, 2, ...] basically
        list of integers as column headers.
        """
        return pd.read_csv(
            self.input_file,
            keep_default_na=self.keep_default_na,
            skip_blank_lines=self.skip_blank_lines,
            header=self.header_row_index,
            encoding=self.encoding,
            delimiter=self.delimiter,
            nrows=0
        ).columns.to_list()

    def _read_dataframe(self,
                        row_idx_to_start_reading,
                        rows_to_read,
                        verbose=True):
        try:
            df = pd.read_csv(
                self.input_file,
                keep_default_na=self.keep_default_na,
                skip_blank_lines=self.skip_blank_lines,
                header=None,
                encoding=self.encoding,
                delimiter=self.delimiter,
                skiprows=row_idx_to_start_reading,
                nrows=rows_to_read
            )

            df = self._assign_column_headers(df)
            if verbose:
                self.logger.info(
                    f"Reading data between row range: {row_idx_to_start_reading+1} "
                    f"=> {row_idx_to_start_reading+rows_to_read}")
        except EmptyDataError:
            # Nothing more to read, thus returns an empty data frame
            return pd.DataFrame(columns=self.headers)

        return df
