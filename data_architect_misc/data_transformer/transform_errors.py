
#
# COLUMNS_TO_USE_TYPE_ERROR = """ERROR: For '""" + KEY_COLUMN_NAMES_TO_USE
# + """' and '""" + KEY_COLUMN_INDEXES_TO_USE + """' keys in JSON
# configuration file, you must provide either 'None' OR
# a list (of *all* strings or *all* integers) for their corresponding values"""

import pdb

class TransformError(Exception):
   """Base class for exceptions"""
   def __str__(self):
       return '->'.join(self.args)


class ConfigFileError(TransformError):
    """Raised when JSON config file is not found or its path is not provided"""
    def __str__(self):
        return "You must provide valid path AND name of " \
               "the JSON configuration file. Try \n>> python " \
               "transform.py -h \nto learn the proper usage."


class FileNotFound(TransformError):
    """Raised when the file(s) is not found"""
    def __init__(self, filename):
        super().__init__("Please make sure that the following file(s) exists:",
                          filename)


class InvalidFileType(TransformError):
    """Raised when the user provide anything beside Excel or CSV file type"""
    def __str__(self):
        return "Program only accepts either Excel or CSV files."

# COLUMNS_TO_USE_KEYS_ERROR = """ERROR: You can provide EITHER """ \
#                    + KEY_COLUMN_NAMES_TO_USE + """ OR """ \
#                    + KEY_COLUMN_INDEXES_TO_USE \
#                    + """in the JSON configuration file. Not both.
#                    If you don't provide either, the program will
#                    parse ALL columns in the file."""
class RedundantJSONKeyError(TransformError):
    """Raised when the config file has more than one key that serves the same
    purpose. For example, we must only provide either sheet name
    OR sheet index. NOT both."""
    def __init__(self, key1, key2):
        self.k1 = key1
        self.k2 = key2

    def __str__(self):
        return ' '.join(['You can provide EITHER', self.k1,
                        'OR', self.k2,
                        'in the JSON configuration file. Not both.'])
