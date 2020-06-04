"""
Author: Phyo Thiha
Last Modified Date: May 05, 2020
"""
import logging

import pandas as pd

from data_readers.pandas_file_data_reader import PandasFileDataReader


class PandasExcelDataReader(PandasFileDataReader):
    """
    This class uses Pandas read_excel to read Pandas dataframe
    from an Excel file. It supports a few most commonly-used
    parameters of read_excel which are defined as class
    CONSTANTS below.
    """
    # Parameters supported from Pandas' read_excel method
    KEY_SHEET_NAME = 'input_sheet_name'
    DEFAULT_SHEET_TO_READ = 0

    def __init__(self, input_file_path_and_name, config):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.input_file = input_file_path_and_name
        self.sheet_name = self._get_sheet_name(config)
        self.headers = self.read_header_row()
        # Number of times read_next_dataframe is called
        self.read_iter_count = 0

    def _get_sheet_name(self, config):
        """Extracts the sheet name to read data from."""
        return config.get(self.KEY_SHEET_NAME,
                          self.DEFAULT_SHEET_TO_READ)

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
        return pd.read_excel(
            self.input_file,
            sheet_name=self.sheet_name,
            keep_default_na=self.keep_default_na,
            header=self.header_row_index,
            nrows=0
        ).columns.to_list()

    def _read_dataframe(self,
                        row_idx_to_start_reading,
                        rows_to_read,
                        verbose=True):
        df = pd.read_excel(
            self.input_file,
            sheet_name=self.sheet_name,
            keep_default_na=self.keep_default_na,
            header=None,
            skiprows=row_idx_to_start_reading,
            nrows=rows_to_read
        )

        if not df.empty:
            df = self._assign_column_headers(df)
            if verbose:
                self.logger.info(
                    f"Reading data between row range:{row_idx_to_start_reading+1} "
                    f"=> {row_idx_to_start_reading+rows_to_read}")

        return df
