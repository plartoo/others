"""
Author: Phyo Thiha
Last Modified Date: April 14, 2020
"""
import os

from data_readers.pandas_excel_data_reader import PandasExcelDataReader
from data_readers.pandas_csv_data_reader import PandasCSVDataReader


def _extract_file_name(file_path_and_name):
    """Extracts file name from path+filename string."""
    return os.path.split(file_path_and_name)[-1]


def _get_file_extension(file_name):
    """Extracts file extension from filename string."""
    return os.path.splitext(file_name)[1]


class FileDataReader:
    """
    This Factory class will be used to generate and
    return different kind of Reader classes such as
    ExcelReader, CSVReader, etc.

    The input parameters to instantiate this class are
    the input file's path+name and a JSON config,
    which has the key-value pairs for other required
    parameters for different reader classes this
    factory class generates.
    """
    CSV_FILE_EXTENSION = '.csv'
    EXCEL_FILE_EXTENSION_OLD = '.xls'
    EXCEL_FILE_EXTENSION_NEW = '.xlsx'

    def __init__(self, input_file_path_and_name, configs):
        self._get_data_reader(input_file_path_and_name, configs)

    def _get_data_reader(self, input_file_path_and_name, configs):
        """
        Factory method that returns the fitting
        data reader object based on the type of
        input file.
        """
        if self._is_excel(input_file_path_and_name):
            return PandasExcelDataReader(input_file_path_and_name, configs)
        elif self._is_csv(input_file_path_and_name):
            return PandasCSVDataReader(input_file_path_and_name, configs)

    def _is_excel(self, file_name_with_path):
        """Checks if file is an Excel file *by checking its file extension*"""
        file_extension = _get_file_extension(
            _extract_file_name(file_name_with_path))
        return ((self.EXCEL_FILE_EXTENSION_NEW == file_extension.lower()) or
                (self.EXCEL_FILE_EXTENSION_OLD == file_extension.lower()))

    def _is_csv(self, file_name_with_path):
        """Checks if file is a CSV file *by checking its file extension*"""
        file_extension = _get_file_extension(
            _extract_file_name(file_name_with_path))
        return self.CSV_FILE_EXTENSION == file_extension.lower()
