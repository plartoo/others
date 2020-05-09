import logging

from data_writers.file_data_writer import FileDataWriter


class CSVDataWriter(FileDataWriter):
    """
    This class is a wrapper to pandas' to_csv' method.
    We can use this class to write dataframe to CSV file as output.
    """

    # Default values for  pandas' to_csv related parameters.
    # We can later implement other pandas.to_csv parameters
    # such as na_rep, compression, quoting, quotechar, etc.
    KEY_OUTPUT_CSV_DELIMITER = 'output_delimiter'
    DEFAULT_OUTPUT_CSV_DELIMITER = '|'

    OUTPUT_FILE_EXTENSION = '.csv'

    def __init__(self, config):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.output_csv_delimiter = config.get(
            self.KEY_OUTPUT_CSV_DELIMITER,
            self.DEFAULT_OUTPUT_CSV_DELIMITER)

    def _get_output_file_extension(self):
        return self.OUTPUT_FILE_EXTENSION

    def write_data(self, df, output_file_path_and_name=None):
        if not output_file_path_and_name:
            out_file = self._get_output_file_path_and_name()
        else:
            out_file = output_file_path_and_name

        self.logger.info(f"Writing data to: {out_file}")
        df.to_csv(
            out_file,
            sep=self.output_csv_delimiter,
            line_terminator='',
            index=self.include_index,
            encoding=self.output_file_encoding
        )
