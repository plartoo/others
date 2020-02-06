class TransformError(Exception):
   """Base class for exceptions."""
   def __str__(self):
       return '-> '.join(self.args)


class ConfigFileError(TransformError):
    """Raised when JSON config file is not found or its path is not provided."""
    def __str__(self):
        return "\nYou must provide valid path AND name of " \
               "the JSON configuration file. Try \n>> python " \
               "transform.py -h \nto learn the proper usage."


class FileNotFound(TransformError):
    """Raised when file(s) is not found."""
    def __init__(self, filename):
        super().__init__("\nPlease make sure that the following file(s) exists ",
                          filename)


class InvalidFileType(TransformError):
    """Raised when the user provide input file that is NOT Excel or CSV."""
    def __init__(self, file_name):
        self.file_name = file_name

    def __str__(self):
        return ' '.join(["\nThis program only accepts either Excel or CSV files.",
                        "But the input file type does not match what's expected:",
                        self.file_name])


class RequiredKeyNotFoundInConfigFile(TransformError):
    """
    Raised when config file does not have required key.
    """
    def __init__(self, key_name):
        self.key_name = key_name

    def __str__(self):
        return ' '.join(["\nPlease make sure to include and provide value for this "
                         "required key in JSON config file:", self.key_name])


class MutuallyExclusiveKeyError(TransformError):
    """
    Raised when config file has more than one key that serves the same
    purpose. For example, we must only provide either the sheet name
    OR sheet index. NOT both.
    """
    def __init__(self, key1, key2):
        self.k1 = key1
        self.k2 = key2

    def __str__(self):
        return ' '.join(["\nYou can provide EITHER '",
                         self.k1,
                        "' OR '",
                         self.k2,
                        "' in JSON configuration file. NOT both."])


class InputDataTypeError(TransformError):
    """
    Raised when config file input is of unexpected data type.
    For example, only 'None' or a 'list' (of *all* strings or
    *all* integers) are allowed for column name and column index
    keys in the config file.
    """
    def __init__(self, key, expected_data_types):
        self.k = key
        self.dt = expected_data_types

    def __str__(self):
        return ''.join(["\nFor '",
                         self.k,
                         "' key in JSON config file, the data type must be one of the following in the list: ",
                         str(self.dt)])


class ListEmptyError(TransformError):
    """Raised when the provided list is empty."""
    def __init__(self, key_name):
        super().__init__("\nPlease make sure that non-empty list is provided for the following key in the config file ",
                          key_name)


#
# COLUMNS_TO_USE_TYPE_ERROR = """ERROR: For '""" + KEY_COLUMN_NAMES_TO_USE
# + """' and '""" + KEY_COLUMN_INDEXES_TO_USE + """' keys in JSON
# configuration file, you must provide either 'None' OR
# a list (of *all* strings or *all* integers) for their corresponding values"""
