"""
Author: Phyo Thiha
Last Modified Date: April 22, 2020
"""
from datetime import datetime
import logging
import os


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
        self.sheet_name = self._get_sheet_name(config)
        # import pdb
        # pdb.set_trace()
        # print("Hey it's Excel reader class")
        self.get_next_dataframe(input_file_path_and_name, config)

    def _get_sheet_name(self, config):
        """
        Extracts sheet name to read data from.
        """
        return config.get(self.KEY_SHEET_NAME,
                          self.DEFAULT_SHEET_TO_READ)

    def read_header_row(self):
        # return pd.read_excel(file_name_with_path,
        #                      skiprows=skip_leading_rows,
        #                      nrows=rows_to_read,
        #                      skipfooter=skip_trailing_rows,
        #                      header=header_row_index,
        #                      names=custom_header_names,
        #                      usecols=column_names_or_indexes_to_use,
        #                      dtype=custom_data_types,
        #                      sheet_name=get_input_file_sheet_name(config),
        #                      )
        pass

    def reader_next_dataframe(self, config):
        # TODO
        pass
        # import pdb
        # pdb.set_trace()
        # print("Hey it's get_next_dataframe")


#col_headers_from_input_file = transform_utils.get_raw_column_headers(input_file, config)
