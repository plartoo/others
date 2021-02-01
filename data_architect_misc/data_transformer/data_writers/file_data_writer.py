from datetime import datetime
import logging
import os


class FileDataWriter:
    """
    This class is the parent class of other data writer classes
    (e.g., ExcelDataWriter or CSVDataWriter) that writes Pandas
    dataframe to an output file.
    """
    # Pandas dataframe has 'index' column
    # This parameter is best left as default, False.
    # Index column, in my opinion, is annoying in output file.
    KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE = 'include_index_column_in_output'
    DEFAULT_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE = False

    # Parameters for output file name and path.
    # User can provide both output file path and name using the key below
    KEY_OUTPUT_FILE_PATH_AND_NAME = 'output_file_name_and_path'

    # Or provide parts of the output file path and name using keys below
    KEY_OUTPUT_FOLDER_PATH = 'output_folder_path'
    DEFAULT_OUTPUT_FOLDER_PATH = os.path.join(os.getcwd(),
                                              'output')
    KEY_OUTPUT_FILE_PREFIX = 'output_file_name_prefix'
    KEY_OUTPUT_FILE_NAME = 'output_file_name'
    KEY_OUTPUT_FILE_SUFFIX = 'output_file_name_suffix'

    # Best leave default as None for encoding
    # because it defaults to 'utf-8'
    # in Pandas's to_excel and to_csv methods
    KEY_OUTPUT_FILE_ENCODING = 'output_encoding'
    DEFAULT_OUTPUT_FILE_ENCODING = None

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)

        self.output_file_path_and_name = config.get(self.KEY_OUTPUT_FILE_PATH_AND_NAME)
        self.output_folder = self._get_output_folder(config)
        self.output_file_name_prefix = config.get(self.KEY_OUTPUT_FILE_PREFIX, '')
        self.output_file_name = config.get(self.KEY_OUTPUT_FILE_NAME, '')
        self.output_file_name_suffix = config.get(self.KEY_OUTPUT_FILE_SUFFIX, '')

        self.include_index = config.get(
            self.KEY_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE,
            self.DEFAULT_INCLUDE_INDEX_COLUMN_IN_OUTPUT_FILE)

        # Encoding of the resulting excel file.
        # Only necessary for xlwt writer engine.
        # Other data_writers support unicode natively.
        self.output_file_encoding = config.get(
            self.KEY_OUTPUT_FILE_ENCODING,
            self.DEFAULT_OUTPUT_FILE_ENCODING)

    def set_output_file_name_prefix(self, prefix_str):
        """
        Setter for output_file_name_prefix class variable.
        This can be used if user decides to change the
        prefix string dynamically (e.g., update prefix
        each time write_data is called).
        """
        self.output_file_name_prefix = prefix_str

    def set_output_file_name_suffix(self, suffix_str):
        """
        Setter for output_file_name_suffix class variable.
        This can be used if user decides to change the
        suffix string dynamically (e.g., update suffix
        each time write_data is called).
        """
        self.output_file_name_suffix = suffix_str

    def _get_output_file_extension(self):
        """
        This method should be implemented by
        classes that inherit this class.
        """
        pass

    def _get_output_folder(self, config):
        """
        Extracts the output folder path and name from the config JSON.
        If the output folder does NOT exist already, this method
        creates one.

        If the keys aren't defined in the JSON config file,
        this method returns default output folder value: ./output
        """
        output_folder = config.get(self.KEY_OUTPUT_FOLDER_PATH,
                                   self.DEFAULT_OUTPUT_FOLDER_PATH)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            self.logger.info(f"New folder created for output files: "
                             f"{output_folder}")
        return output_folder

    def _get_output_file_name(self):
        """
        Joins output file name prefix (e.g., 'my_output_file*')
        and suffix (e.g., '_0_500_lines'), if any of them is
        provided, with current datetime in YYYYMMDD_HHMMSS format
        as the last suffix and returns the result as output file name.
        """
        datetime_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Only select the non-empty strings from the file name parts
        output_file_name = '_'.join([a for a in
                                     [self.output_file_name_prefix, self.output_file_name,
                                      self.output_file_name_suffix, datetime_suffix] if a
                                     ])

        return f"{output_file_name}{self._get_output_file_extension()}"

    def _get_output_file_path_and_name(self):
        """
        Returns the full output file path and name by joining
        output folder; file name prefix, if any; and file name
        suffix, which is just timestamp in the form of
        YYYYMMDD_HHMMSS.
        """
        if self.output_file_path_and_name is not None:
            # If user provides output file path and name via commandline
            return self.output_file_path_and_name
        else:
            # if the user
            return os.path.join(self.output_folder,
                                self._get_output_file_name())
