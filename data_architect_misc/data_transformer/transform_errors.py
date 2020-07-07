class TransformError(Exception):
    """Base class for transform class related exceptions."""

    def __str__(self):
        return f"\nERROR: {''.join(self.args)}"


class ConfigFileError(TransformError):
    """
    Raised when JSON config file is not found
    or its path is not provided.
    """

    def __str__(self):
        return f"You must provide valid path AND name of " \
               f"the JSON configuration file. Try \n>> python " \
               f"transform.py -h \nto learn the proper usage."


class FileNotFound(TransformError):
    """Raised when file(s) is not found."""

    def __init__(self, filename):
        super().__init__(f"Please make sure that the following "
                         f"file(s) exists: {filename}")


class InvalidFileType(TransformError):
    """
    Raised when the user provide input file
    that is NOT Excel or CSV.
    """

    def __init__(self, file_name):
        self.file_name = file_name

    def __str__(self):
        return f"This program only accepts either Excel or CSV files. " \
               f"Here, this input file type is neither Excel nor CSV: " \
               f"{self.file_name}"


class RequiredKeyNotFound(TransformError):
    """
    Raised when we do NOT find required key in a dictionary.
    """

    def __init__(self, dictionary, key_names):
        self.dictionary = dictionary
        self.key_names = key_names

    def __str__(self):
        return f"In dictionary: {self.dictionary}, at least one of the " \
               f"following required keys(s) must exist: {self.key_names}"


class RequiredKeyNotFoundInConfigFile(TransformError):
    """
    Raised when config file does not have required key
    (more specific version of RequiredKeyNotFound error).
    """

    def __init__(self, key_name):
        self.key_name = key_name

    def __str__(self):
        return f"Please make sure to include and provide value for this " \
               f"required key in JSON config file: {self.key_name}"


class ReservedKeywordConflictForMetaConfigError(TransformError):
    """
    Raised when somebody mistakenly use the reserved
    keyword, which is used to pass down the meta-level
    config information into transform functions.

    For more info, read transform.py file code where we
    pass down func_args and func_kwargs to transform
    function.
    """
    def __init__(self, key_name_in_conflict, function_kwarg):
        self.key_name_in_conflict = key_name_in_conflict
        self.function_kwarg = function_kwarg

    def __str__(self):
        return f"You cannot use the keyword, '{self.key_name_in_conflict}'" \
               f", which is reserved to pass down " \
               f"the configs (from the JSON config file) into " \
               f"transform functions. Try renaming the key in this functions' " \
               f"kwargs in your JSON config file to something different: " \
               f"{self.function_kwarg}."


class ConfigFileInputDataTypeError(TransformError):
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
        return f"For {self.k} key in JSON config file, the data type " \
               f"must be one of the followings: {self.dt}"


class InputDataTypeError(TransformError):
    """Raised when the data type of the input parameter do not match what is expected.
    """

    def __init__(self, error_msg):
        super().__init__(error_msg)


class InputDataLengthError(TransformError):
    """Raised when the length of the input parameter do not match what is expected.
    """

    def __init__(self, error_msg):
        super().__init__(error_msg)


class ListEmptyError(TransformError):
    """Raised when the provided list is empty."""

    def __init__(self, key_name):
        super().__init__(f"Please make sure that non-empty list "
                         f"is provided for the following key "
                         f"in the config file: {key_name}")


class OrderOfListContentsDifferentError(TransformError):
    """
    Raised when the order of the contents in
    two lists are NOT the the same.
    """

    def __init__(self, list1, list2):
        super().__init__(f"The order of contents in these two lists "
                         f"are NOT the same as expected:\n"
                         f"{list1}\n"
                         f"{list2}.")

# class MutuallyExclusiveKeyError(TransformError):
#     """
#     Raised when config file has more than one key that serves the same
#     purpose. For example, we must only provide either the sheet name
#     OR sheet index. NOT both.
#
#     NOTE: No longer used because I redesigned the config file keys
#     so that we don't need to have mutually exclusive keys anymore.
#     """
#     def __init__(self, key1, key2):
#         self.k1 = key1
#         self.k2 = key2
#
#     def __str__(self):
#         return f"You can provide EITHER {self.k1} OR {self.k2}" \
#                f"in JSON configuration file. NOT BOTH."
