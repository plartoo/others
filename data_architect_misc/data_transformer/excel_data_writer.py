import logging

from file_data_writer import FileDataWriter


class ExcelDataWriter(FileDataWriter):
    """
    This class is a wrapper to pandas' to_excel' method.
    We can use this class to write dataframe to Excel file as output.
    """

    # Default values for  pandas' to_excel related parameters.
    # We can add other params such as na_rep, columns, header, etc. later.
    KEY_SHEET_NAME_OF_OUTPUT_EXCEL_FILE = 'sheet_name_of_output_excel_file'
    DEFAULT_SHEET_NAME_OF_OUTPUT_EXCEL_FILE = 'Sheet1'

    def __init__(self, config):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.sheet_name = config.get(
            self.KEY_SHEET_NAME_OF_OUTPUT_EXCEL_FILE,
            self.DEFAULT_SHEET_NAME_OF_OUTPUT_EXCEL_FILE)

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
            encoding=self.output_file_encoding
        )
