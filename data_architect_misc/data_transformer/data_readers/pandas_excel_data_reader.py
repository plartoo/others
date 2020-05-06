"""
Author: Phyo Thiha
Last Modified Date: April 22, 2020
"""
import logging

import pandas as pd
from rich import print

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
        self.header_row = self.read_header_row()
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
            header=self.header_row_index,
            nrows=0
        ).columns.to_list()

    def _assign_column_headers(self, df):
        """
        We read column headers once from
        the row defined in the config.
        Then we apply these column headers
        to dataframe read chunk by chunk.
        """
        df.columns = self.header_row
        return df

    def _get_row_idx_to_start_reading(self):
        """
        Updates value that keeps track of which row
        we should start reading data from if
        read_next_dataframe is called again.
        """
        return (self.rows_per_read
                * self.read_iter_count) \
               + self.skip_rows

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
                print(f"Read data from row:{row_idx_to_start_reading+1} "
                      f"=> {row_idx_to_start_reading+rows_to_read}")

        return df

    def _read_one_line_ahead(self):
        """
        This method is used to check if the dataframe
        we'll be reading in the next iteration is
        empty.
        """
        return self._read_dataframe(
            self._get_row_idx_to_start_reading(),
            1,
            False)

    def read_next_dataframe(self):
        df = self._read_dataframe(self._get_row_idx_to_start_reading(),
                                  self.rows_per_read)

        # Increment counter below to prepare for the next read
        self.read_iter_count += 1

        if (self.skip_footer > 0) and self._read_one_line_ahead().empty:
            # Here, the user needs to be careful that rows
            # to drop from the bottom, 'skipfooter',
            # do not awkwardly fall between the previously
            # read dataframe and the next one to read. If
            # they do, then this will only drop fewer than
            # self.skip_footer rows.
            #
            # In other words, user needs to make sure the
            # 'rows_per_read' and 'skipfooter' don't conflict
            # each other and thus, resulting in some rows
            # from the bottom not being dropped.
            # See 'TestExcelFile2.xlsx' and 'TestExcelConfig2.json'
            # in examples/test folder as an example of this
            # awkward scenario.

            print(f"Dropped *as many as* (could be fewer than) "
                  f"this number of rows of data: "
                  f"{self.skip_footer}")
            # REF: https://stackoverflow.com/a/57681199
            return df[:-self.skip_footer]

        return df
