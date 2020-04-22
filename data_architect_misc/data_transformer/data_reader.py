"""
Author: Phyo Thiha
Last Modified Date: April 14, 2020
"""
import os


class DataReader:
    """
    Factory class that will be used to generate and
    return different kind of Reader classes such as
    ExcelReader, CSVReader, etc.

    The input parameter to instantiate this class is
    a JSON config, which has at least the key-value
    pairs for input file name, file path (folder), and
    other required key-value pairs for different reader
    classes this factory class generates.
    """
    # Other constants
    CSV_FILE_EXTENSION = '.csv'
    EXCEL_FILE_EXTENSION_OLD = '.xls'
    EXCEL_FILE_EXTENSION_NEW = '.xlsx'

    # TODO: move constants into something like 'config_constants.py'
    def __init__(self, input_file_path_and_name, **configs):

        pass

    def _get_data_reader(self, input_file_path_and_name, **configs):
        """
        Factory method that returns the fitting
        data reader object based on the type of
        input file.
        """
        if self._is_excel(input_file_path_and_name):
            return ExcelReader(input_file_path_and_name, **configs)
        elif self._is_csv(input_file_path_and_name):
            return CSVReader(input_file_path_and_name, **configs)

    def _extract_file_name(file_path_and_name):
        """Extracts file name from path+filename string."""
        return os.path.split(file_path_and_name)[-1]

    def _get_file_extension(file_name):
        """Extracts file extension from filename string."""
        return os.path.splitext(file_name)[1]

    def _is_excel(self, file_name_with_path):
        """Checks if file is an Excel file *by checking its file extension*"""
        file_extension = self._get_file_extension(
            self._extract_file_name(file_name_with_path))
        return ((self.EXCEL_FILE_EXTENSION_NEW == file_extension.lower()) or
                (self.EXCEL_FILE_EXTENSION_OLD == file_extension.lower()))

    def _is_csv(self, file_name_with_path):
        """Checks if file is a CSV file *by checking its file extension*"""
        file_extension = self._get_file_extension(
            self._extract_file_name(file_name_with_path))
        return self.CSV_FILE_EXTENSION == file_extension.lower()


class ExcelReader:
    """
    TODO:
    """
    SHEET_NAME = 'sheet_name'
    DEFAULT_SHEET_INDEX_TO_READ = 0

    def __init__(self, input_file_path_and_name, **configs):
        import pdb
        pdb.set_trace()
        print("Hey it's Excel reader class")
        pass


class CSVReader:
    """
    TODO:
    """
    KEY_INPUT_CSV_DELIMITER = 'input_csv_file_delimiter'
    DEFAULT_INPUT_CSV_DELIMITER = ','
    KEY_OUTPUT_CSV_DELIMITER = 'output_csv_file_delimiter'
    DEFAULT_OUTPUT_CSV_DELIMITER = '|'
    DEFAULT_SHEET_INDEX_TO_READ = 0

    def __init__(self, input_file_path_and_name, **configs):
        import pdb
        pdb.set_trace()
        print("Hey it's Excel reader class")
        pass
