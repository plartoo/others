"""
Author: Phyo Thiha
Last Modified Date: April 22, 2020
"""
import logging

import pandas as pd

from data_readers.pandas_file_data_reader import PandasFileDataReader


class PandasExcelDataReader(PandasFileDataReader):
    """
    This class uses Pandas read_excel to read Pandas dataframe
    from an Excel file. It supports several most commonly-used
    parameters of read_excel which are defined as class
    CONSTANTS below.
    """
    # Parameters supported from Pandas' read_excel method
    KEY_SHEET_NAME = 'sheet_name' # 'sheet_name_of_input_excel_file'
    DEFAULT_SHEET_TO_READ = 0

    def __init__(self, input_file_path_and_name, config):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.input_file = input_file_path_and_name
        self.sheet_name = self._get_sheet_name(config)
        self.header_row = self.read_header_row()
        # number of times read_next_dataframe is called
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
            header=self.header_row_index,
            nrows=0
        ).columns.to_list()

    def _get_row_idx_to_start_reading(self):
        """
        Updates value that keeps track of which row
        we should start reading data from if
        read_next_dataframe is called again.
        """
        return (self.rows_per_read
                * self.read_iter_count) \
               + self.skip_rows

    def read_next_dataframe(self):
        row_idx_to_start_reading = self._get_row_idx_to_start_reading()
        print(f"reading rows:{row_idx_to_start_reading}")
        df = pd.read_excel(
            self.input_file,
            sheet_name=self.sheet_name,
            keep_default_na=self.keep_default_na,
            header=None,
            skiprows=row_idx_to_start_reading,
            nrows=self.rows_per_read
        )
        self.read_iter_count += 1
        print(df)
        import pdb
        pdb.set_trace()
        print("Hey it's get_next_dataframe")
        return df

        # TODO: we will drop rows for skipfooter based on calculation later

        pass
        # cur_df = pd.read_excel(
        #   input_file,
        #   sheet_name=sheet,
        #   keep_default_na=keep_default_na,
        #   skiprows=row_idx_where_data_starts,
        #   skipfooter=footer_rows_to_skip,
        #   header=None,
        #   names=col_headers_from_input_file)

#col_headers_from_input_file = transform_utils.get_raw_column_headers(input_file, config)
