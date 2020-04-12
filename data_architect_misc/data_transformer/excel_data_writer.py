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
    def __init__(self, config):
        # We can later implement other pandas.to_excel parameters
        # such as na_rep, columns, header, etc.
        self.output_file_path_and_name = self.get_output_file_path_and_name(config)
        self.include_index = self.get_include_index_column_in_output_excel_file(config)
        # Encoding of the resulting excel file.
        # Only necessary for xlwt, other writers support unicode natively.
        self.output_file_encoding = self.get_output_excel_file_encoding(config)
        self.sheet_name = self.get_output_excel_file_sheet_name(config)
        self.logger = logging.getLogger(__name__)


    @staticmethod
    def get_output_file_path_and_name(config):
        """
        Returns output file path with file name prefix, if the latter
        is provided in the config JSON. Before joining the path with
        file name, output folder is created if it doesn't exist already.
        """
        logger = logging.getLogger(__name__)
        output_folder = transform_utils.get_output_folder(config)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            logger.info(f"New folder created for output files: {output_folder}")

        file_prefix = transform_utils.get_output_file_prefix(config)
        file_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file_name = ''.join(['_'.join([file_prefix, file_suffix]), '.xlsx'])

        return os.path.join(output_folder, output_file_name)


    @staticmethod
    def get_include_index_column_in_output_excel_file(config):
        """
        Extracts and return boolean value to decide if output Excel
        file should include index column from the dataframe.
        """
        return transform_utils.get_include_index_column_in_output(config)


    @staticmethod
    def get_output_excel_file_encoding(config):
        """
        Extracts and return encoding string value for output Excel file.
        Defaults to None because it is (strangely) equivalent to 'utf-8'
        in Pandas.
        """
        return transform_utils.get_output_file_encoding(config)


    @staticmethod
    def get_output_excel_file_sheet_name(config):
        """
        Extracts and return sheet name (string) for output Excel file.
        Defaults to None because it is (strangely) equivalent to 'utf-8'
        in Pandas.
        """
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
        self.logger.info(f"Writing data to: {self.output_file_path_and_name}")
        df.to_excel(
            self.output_file_path_and_name,
            sheet_name=self.sheet_name,
            index=self.include_index,
            encoding=self.output_file_encoding
        )
