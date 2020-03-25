from datetime import datetime
import os

import pandas as pd

import transform_utils


class CSVDataWriter:
    """
    This class the parent class of DataWriter, which is required
    to write data from Pandas dataframe to CSV file.
    Here, we only use this class to set up necessary
    parameters for pandas.to_csv method and implement
    write_data() method in its child class, DataWriter.
    (I admit it's a bit funny that the parent class has
    more specific name than child class, but I figured
    it's better to do it this way for a couple of
    different reasons, which I will not explain further here.)
    """
    def __init__(self, config):
        # We can later implement other pandas.to_csv parameters
        # such as na_rep, compression, quoting, quotechar, etc.
        self.output_file_path_and_name = self.get_output_file_path_and_name(config)
        self.include_index = self.get_include_index_column_in_output_csv_file(config)
        self.output_file_encoding = self.get_output_csv_file_encoding(config)
        self.output_file_delimiter = self.get_output_csv_file_delimiter(config)


    @staticmethod
    def get_output_file_path_and_name(config):
        """
        Returns output file path with file name prefix, if the latter
        is provided in the config JSON. Before joining the path with
        file name, output folder is created if it doesn't exist already.
        """
        output_folder = transform_utils.get_output_folder(config)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print("\nINFO: new folder created for output files =>", output_folder)

        file_prefix = transform_utils.get_output_file_prefix(config)
        file_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file_name = ''.join(['_'.join([file_prefix, file_suffix]), '.csv'])

        return os.path.join(output_folder, output_file_name)


    @staticmethod
    def get_include_index_column_in_output_csv_file(config):
        """
        Extracts and return boolean value to decide if output CSV
        file should include index column from the dataframe.
        """
        return transform_utils.get_include_index_column_in_output(config)


    @staticmethod
    def get_output_csv_file_encoding(config):
        """
        Extracts and return encoding string value for output CSV file.
        Defaults to None because it is (strangely) equivalent to 'utf-8'
        in Pandas.
        """
        return transform_utils.get_output_file_encoding(config)


    @staticmethod
    def get_output_csv_file_delimiter(config):
        """
        Extracts and return delimiter (string) value for output CSV file.
        Defaults to ',' (comma).
        """
        return transform_utils.get_output_csv_file_delimiter(config)


class DataWriter(CSVDataWriter):
    """
    This class is the child class of CSVDataWriter.
    Anyone who wants to implement other custom DataWriter class
    must make sure that it implements write_data(dataframe) method
    because it is expected in transform.py file.
    """

    def __init__(self, config):
        super().__init__(config)


    def write_data(self, df):
        print("Writing data to:", self.output_file_path_and_name)
        df.to_csv(
            self.output_file_path_and_name,
            index=self.include_index,
            sep=self.output_file_delimiter,
            encoding=self.output_file_encoding
        )
