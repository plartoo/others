"""
Author: Phyo Thiha
Last Modified Date: April 14, 2020
"""


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
    def __init__(self, config):
        # TODO: move constants into something like 'config_constants.py'
        pass
