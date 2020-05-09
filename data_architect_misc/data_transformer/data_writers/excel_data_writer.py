import logging

from data_writers.file_data_writer import FileDataWriter


class ExcelDataWriter(FileDataWriter):
    """
    This class is a wrapper to pandas' to_excel' method.
    We can use this class to write dataframe to Excel file as output.
    """

    # Default values for  pandas' to_excel related parameters.
    # We can add other params such as na_rep, columns, header, etc. later.
    KEY_SHEET_NAME_OF_OUTPUT_EXCEL_FILE = 'output_sheet_name'
    DEFAULT_SHEET_NAME_OF_OUTPUT_EXCEL_FILE = 'Sheet1'

    OUTPUT_FILE_EXTENSION = '.xlsx'

    def __init__(self, config):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.sheet_name = config.get(
            self.KEY_SHEET_NAME_OF_OUTPUT_EXCEL_FILE,
            self.DEFAULT_SHEET_NAME_OF_OUTPUT_EXCEL_FILE)

    def _get_output_file_extension(self):
        return self.OUTPUT_FILE_EXTENSION

    def write_data(self, df, output_file_path_and_name=None):
        if not output_file_path_and_name:
            out_file = self._get_output_file_path_and_name()
        else:
            out_file = output_file_path_and_name

        self.logger.info(f"Writing data to: {out_file}")
        df.to_excel(
            out_file,
            sheet_name=self.sheet_name,
            index=self.include_index,
            # For to_excel method, encoding parameter is
            # only necessary for xlwt writer. Otherwise,
            # we can leave it as None by default (which
            # is what we defined in FileDataWriter)
            # REF: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html
            encoding=self.output_file_encoding
        )
