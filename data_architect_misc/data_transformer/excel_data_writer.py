from datetime import datetime
import logging
import os

import transform_utils


class ExcelDataWriter:
    """
    This class the parent class of DataWriter, which is required
    to write data from Pandas dataframe to Excel file.
    Here, we only use this class to set up necessary
    parameters for pandas.to_excel method and implement
    write_data() method in its child class, DataWriter.
    """
    DEFAULT_OUTPUT_FILE_ENCODING = None  # None defaults to 'utf-8' in pandas
    KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE = 'include_index_column_in_output'
    DEFAULT_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE = False

    KEY_OUTPUT_FOLDER_PATH = 'output_folder_path'
    DEFAULT_OUTPUT_FOLDER_PATH = os.path.join(os.getcwd(),
                                              'output')
    KEY_OUTPUT_FILE_PREFIX = 'output_file_name_prefix'
    KEY_OUTPUT_FILE_ENCODING = 'output_file_encoding'
    KEY_SHEET_NAME_OF_OUTPUT_EXCEL_FILE = 'sheet_name_of_output_excel_file'
    DEFAULT_SHEET_NAME_OF_OUTPUT_EXCEL_FILE = 'Sheet1'

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.output_folder = self._get_output_folder(config)
        self.output_file_prefix = self._get_output_file_name_prefix(config)
        # We can later implement other pandas.to_excel parameters
        # such as na_rep, columns, header, etc.
        self.include_index = self._get_include_index_column_in_output_excel_file(config)
        # Encoding of the resulting excel file.
        # Only necessary for xlwt, other writers support unicode natively.
        self.output_file_encoding = self._get_output_excel_file_encoding(config)
        self.sheet_name = self._get_output_excel_file_sheet_name(config)

    @staticmethod
    def get_value_from_dict(dictionary, key, default_value):
        """
        Returns associated value of a given key from dict.
        If the key doesn't exist, returns default_value.
        """
        if dictionary.get(key) is None:
            return default_value
        elif (isinstance(dictionary.get(key), str)) and (not dictionary.get(key)):
            return default_value
        else:
            return dictionary.get(key)

    def _get_output_folder(self, config):
        """
        Extracts the output folder path and name from the config JSON.
        If the output folder does NOT exist already, this method
        creates one.

        If the keys aren't defined in the JSON config file,
        this method returns default output folder value: ./output
        """
        output_folder = self.get_value_from_dict(
            config,
            self.KEY_OUTPUT_FOLDER_PATH,
            self.DEFAULT_OUTPUT_FOLDER_PATH)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            self.logger.info(f"New folder created for output files: "
                             f"{output_folder}")
        return output_folder

    def _get_output_file_name_prefix(self, config):
        return self.get_value_from_dict(
            config,
            self.KEY_OUTPUT_FILE_PREFIX,
            '')

    def _get_output_file_name(self):
        """
        Joins output file name prefix, if any, from config JSON
        with current datetime in YYYYMMDD_HHMMSS format and
        returns the result as output file name.
        """
        file_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{self.output_file_prefix}_{file_suffix}.xlsx"

    def _get_output_file_path_and_name(self):
        """
        Returns the full output file path and name by joining
        output folder; file name prefix, if any; and file name
        suffix, which is just timestamp in the form of
        YYYYMMDD_HHMMSS.
        """
        return os.path.join(self.output_folder,
                            self._get_output_file_name())

    def _get_include_index_column_in_output_excel_file(self, config):
        """
        Extracts and return boolean value to decide if output Excel
        file should include index column from the dataframe.
        """
        return self.get_value_from_dict(config,
                                        self.KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE,
                                        self.DEFAULT_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE)

    def _get_output_excel_file_encoding(self, config):
        """
        Extracts and return encoding string value for output Excel file.
        Defaults to None because it is (strangely) equivalent to 'utf-8'
        in Pandas.
        """
        return self.get_value_from_dict(config,
                                        self.KEY_OUTPUT_FILE_ENCODING,
                                        self.DEFAULT_OUTPUT_FILE_ENCODING)

    def _get_output_excel_file_sheet_name(self, config):
        """
        Extracts and return sheet name (string) for output Excel file.
        Defaults to None because it is (strangely) equivalent to 'utf-8'
        in Pandas.
        """
        return self.get_value_from_dict(config,
                                        self.KEY_SHEET_NAME_OF_OUTPUT_EXCEL_FILE,
                                        self.DEFAULT_SHEET_NAME_OF_OUTPUT_EXCEL_FILE)

        return transform_utils.get_output_file_sheet_name(config)


class DataWriter(ExcelDataWriter):
    """
    This class is the child class of ExcelDataWriter.
    Anyone who wants to implement other custom DataWriter class
    must make sure that it implements write_data(dataframe) method
    because it is expected in transform.py file.
    """
    def __init__(self, config):
        super().__init__(config)

    def write_data(self, df):
        output_file_path_and_name = self._get_output_file_path_and_name()
        self.logger.info(f"Writing data to: {output_file_path_and_name}")
        df.to_excel(
            output_file_path_and_name,
            sheet_name=self.sheet_name,
            index=self.include_index,
            encoding=self.output_file_encoding
        )
