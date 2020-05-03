"""
Author: Phyo Thiha
Last Modified Date: May 2, 2020
"""
import logging


class PandasFileDataReader:
    """
    This class is used as parent class to organize
    common parameters and their default values for
    PandasExcelDataReader and PandasCSVDataReader
    (and maybe more if I add more data readers
    based on Pandas' data reader methods later).

    This class takes JSON config as parameter
    that has key-value pairs representing parameter
    names and their values that will be used in
    reading data via Pandas methods.
    """
    KEY_ROWS_PER_READ = 'rows_per_read'
    DEFAULT_ROWS_PER_READ = 500000

    # Parameters below are pandas-related parameters
    # supported by this file reader class' children.
    KEY_KEEP_DEFAULT_NA = 'keep_default_na'
    DEFAULT_KEEP_DEFAULT_NA = False

    KEY_HEADER = 'header'
    DEFAULT_HEADER = None

    KEY_SKIP_ROWS = 'skiprows'
    DEFAULT_SKIP_ROWS = 1

    KEY_SKIP_FOOTER = 'skipfooter'  # 'num_of_rows_to_skip_from_the_bottom'
    DEFAULT_SKIP_FOOTER = 0

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.rows_per_read = self._get_rows_per_read(config)
        self.keep_default_na = self._get_keep_default_na(config)
        self.header = self._get_row_index_to_read_column_header(config)
        self.skip_rows = self._get_leading_rows_to_skip(config)
        self.skip_footer = self._get_bottom_rows_to_skip(config)

    def _get_rows_per_read(self, config):
        """
        Get rows to read per iteration (each read).
        Limiting this to some sensible value (e.g.,
        read no more than 1 million rows per read)
        will keep us away from running out of RAM.
        """
        return config.get(self.KEY_ROWS_PER_READ,
                          self.DEFAULT_ROWS_PER_READ)

    def _get_keep_default_na(self, config):
        """
        Pandas unfortunately has 'keep_default_na' option
        which tries to interpret NaN, NULL, NA, N/A, etc.
        values in the raw data to NaN.

        We must turn it off by default.
        REF: https://stackoverflow.com/a/41417295
        """
        return config.get(self.KEY_KEEP_DEFAULT_NA,
                          self.DEFAULT_KEEP_DEFAULT_NA)

    def _get_row_index_to_read_column_header(self, config):
        """
        By default, assume that there is NO column header.
        Therefore, we set None as default (according to
        the way Pandas uses it) here.

        Otherwise, user is expected to provide index value
        greater than or equal to 0 (i.e. 0 represents
        the first row of the file in Pandas).
        """
        return config.get(self.KEY_HEADER,
                          self.DEFAULT_HEADER)

    def _get_leading_rows_to_skip(self, config):
        """
        By default, we assume that the second row of
        the file is where the data (not the column
        headers) begins. Therefore, we set the default
        value to 1.

        Note: Pandas uses 0-indexed values to
        represent rows, so if the user wants to read
        from the 5th row in the file, this value should
        be set to 4.
        """
        return config.get(self.KEY_SKIP_ROWS,
                          self.DEFAULT_SKIP_ROWS)

    def _get_bottom_rows_to_skip(self, config):
        """
        By default, we assume that no rows from the
        bottom of the file will be skipped in reading.
        Therefore, we set the default value to 0

        Note: Pandas uses 0-indexed values to
        represent rows, so if the user wants to skip
        the last 8 rows, this values should be set to
        7.
        """
        return config.get(self.KEY_SKIP_FOOTER,
                          self.DEFAULT_SKIP_FOOTER)
