from datetime import datetime
import logging
import os


class CSVDataWriter:
    """
    This class the parent class of DataWriter, which is required
    to write data from Pandas dataframe to CSV file.

    Here, we only use this class to set up necessary
    parameters including the ones for pandas.to_csv method.
    We will implement write_data() method in its child class, DataWriter.

    Then we can import and instantiate a specific DataWriter
    module dynamically in another Python module and call write_data().
    An example usage of this class can be found in one of the Python
    modules named 'data_tranformer' in my Github repo.
    """

    # TODO: later, move the following constants into constants_writers.py to be used in both CSV, Excel and so on writers.
    KEY_OUTPUT_CSV_DELIMITER = 'output_csv_file_delimiter'
    DEFAULT_OUTPUT_CSV_DELIMITER = '|'
    KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE = 'include_index_column_in_output'
    DEFAULT_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE = False
    KEY_OUTPUT_FILE_ENCODING = 'output_file_encoding'
    DEFAULT_OUTPUT_FILE_ENCODING = None  # None defaults to 'utf-8' in pandas

    # Parameters for output file name and path.
    KEY_OUTPUT_FOLDER_PATH = 'output_folder_path'
    DEFAULT_OUTPUT_FOLDER_PATH = os.path.join(os.getcwd(),
                                              'output')
    KEY_OUTPUT_FILE_PREFIX = 'output_file_name_prefix'
    KEY_OUTPUT_FILE_SUFFIX = 'output_file_name_suffix'

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)

        # We can later implement other pandas.to_csv parameters
        # such as na_rep, compression, quoting, quotechar, etc.
        self.output_file_path_and_name = self.get_output_file_path_and_name(config)

        self.output_file_delimiter = config.get(
            self.KEY_OUTPUT_CSV_DELIMITER,
            self.DEFAULT_OUTPUT_CSV_DELIMITER)

        # boolean to decide if output file should have index column from the dataframe
        self.include_index = config.get(
            self.KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE,
            self.DEFAULT_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE)

        # Encoding of the resulting excel file.
        # Only necessary for xlwt writer engine.
        # Other writers support unicode natively.
        self.output_file_encoding = config.get(
            self.KEY_OUTPUT_FILE_ENCODING,
            self.DEFAULT_OUTPUT_FILE_ENCODING)

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
        output_file_name = ''.join(['_'.join([file_prefix, file_suffix]), '.csv'])

        return os.path.join(output_folder, output_file_name)



class DataWriter(CSVDataWriter):
    """
    This class is the child class of CSVDataWriter.
    Anyone who wants to implement other custom DataWriter class
    must make sure that it implements write_data(dataframe) method
    because it is expected in transform.py file.
    """

    def __init__(self, config):
        super().__init__(config)

    def write_data(self, df, output_file_path_and_name=None):
        if not output_file_path_and_name:
            out_file = self._get_output_file_path_and_name()
        else:
            out_file = output_file_path_and_name

        self.logger.info(f"Writing data to: {out_file}")
        df.to_csv(
            out_file,
            sep=self.output_file_delimiter,
            index=self.include_index,
            encoding=self.output_file_encoding
        )
