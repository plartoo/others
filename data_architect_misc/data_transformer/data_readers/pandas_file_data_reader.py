"""
Author: Phyo Thiha
Last Modified Date: May 2, 2020
"""
import logging


class ConflictingParametersError(Exception):
    """
    Raise this if the number of rows to read per iteration
    is less than the number of rows to drop at the end of
    the file.

    If we allow that, the implementation will become
    unnecessarily complicated (hard to understand/follow)
    and thus, to keep things simple, we'll just warn the
    user to adjust the rows per read parameter.
    """

    def __init__(self, error_msg):
        super().__init__(error_msg)


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
    DEFAULT_ROWS_PER_READ = 100000

    # Parameters below are pandas-related parameters
    # supported by this file reader class' children.
    KEY_KEEP_DEFAULT_NA = 'keep_default_na'
    DEFAULT_KEEP_DEFAULT_NA = False

    KEY_HEADER = 'header'
    DEFAULT_HEADER = None

    KEY_SKIP_ROWS = 'skiprows'
    DEFAULT_SKIP_ROWS = 1

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
    # See 'excel2.xlsx' and 'excel2_config.json'
    # in 'examples/' folder as an example of this
    # awkward scenario (assuming rows_per_read=10).
    KEY_SKIP_FOOTER = 'skipfooter'  # number of rows to drop from the bottom
    DEFAULT_SKIP_FOOTER = 0

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.rows_per_read = self._get_rows_per_read(config)
        self.keep_default_na = self._get_keep_default_na(config)
        self.header_row_index = self._get_row_index_to_read_column_header(config)
        self.skip_rows = self._get_leading_rows_to_skip(config)
        self.skip_footer = self._get_bottom_rows_to_skip(config)
        if self.rows_per_read < self.skip_footer:
            raise ConflictingParametersError(
                f"The number of rows to read per iteration, "
                f"'{self.rows_per_read}', is less than the number of "
                f"rows to drop at the end of the file, '{self.skip_footer}'. "
                f"Please adjust the '{self.KEY_ROWS_PER_READ}' value "
                f"to be at least greater than or equal to that of "
                f"the '{self.KEY_SKIP_FOOTER}' in the config parameter.")

        # Variables below must be set by child classes
        self.headers = None
        self.read_iter_count = None

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

    def _rename_existing_and_add_new_cols_with_empty_str(self, df):
        """
        In Pandas CSV reader when we read chunk by chunk and
        if the raw data file has rows that do not conform to
        the column width of the others (e.g., the first 5 rows
        in raw data has 5 columns, the next 3 rows have 1 column
        only and if are reading 5 lines per iteration), ValueError
        will be thrown when we assign the chunk with a smaller set
        of actual columns (in the above example, only 1 column) to
        the full set of columns seen in the beginning of the file.

        In that scenario, this program will rename the column of the
        new chunk to conform to the column names of the dataset in
        its entirety (i.t. self.headers) and since the new chunk
        doesn't have data for some of the newly expanded columns
        (in the above example, there will be 4 new columns added),
        it will assign empty string in these columns.

        REF: https://stackoverflow.com/a/61650632/1330974
        """
        return df.rename(columns=dict(zip(df.columns, self.headers)))\
            .reindex(self.headers, axis=1)

    def _assign_column_headers(self, df):
        """
        We read column headers once from
        the row defined in the config.
        Then we apply these column headers
        to dataframe read chunk by chunk.
        """
        try:
            df.columns = self.headers
        except ValueError:
            # This error is usually raised in rare instances
            # when CSV files have some footers rows with
            # fewer columns than the rows above
            # (e.g., Copyrights note at the bottom) and
            # when that row is read on its own chunk.
            self.logger.warning(
                f"The dataframe below have fewer columns "
                f"than other rows in the data:\n"
                f"{df}"
                f"\n-->This is the list of column headers "
                f"expected for the dataframe (based on "
                f"what we have seen in previous dataframes "
                f"or data rows): {self.headers}"
                f"\n-->We will rename and append missing "
                f"columns to the above dataframe with "
                f"empty strings. For more details, please "
                f"see pandas_file_data_reader.py's "
                f"'_assign_column_headers' method.\n"
            )
            return self._rename_existing_and_add_new_cols_with_empty_str(df)

        return df

    def _get_row_idx_to_start_reading(self):
        """
        Updates value that keeps track of which row
        we should start reading data from if
        read_next_dataframe is called again.
        """
        return (self.rows_per_read
                * self.read_iter_count) + self.skip_rows

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
            self.logger.info(
                f"Dropped *as many as* (could be fewer than) "
                f"this number of rows of data: {self.skip_footer}"
                f"\nThe following rows are dropped:\n"
                f"{df[-self.skip_footer:]}")

            # REF: https://stackoverflow.com/a/57681199
            return df[:-self.skip_footer]

        return df
